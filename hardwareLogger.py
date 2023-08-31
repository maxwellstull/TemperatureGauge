# Normal python imports
from classes import OHardware, OSensor, CQueue
import time
import clr
# Dll stuff
clr.AddReference(r'OpenHardwareMonitorLib')
from OpenHardwareMonitor import Hardware 

# Class that handles that connection to openhardwaremonitor and holds objects that track values
class hardwareLogger():
    # Initializer
    # Params: self (duh)
    # Returns: N/A
    def __init__(self):
        start_init = time.time()
        print("Initializing OHM Connection")
        # OHM things
        self.handle = Hardware.Computer()
        self.handle.MainboardEnabled = True
        self.handle.CPUEnabled = True
        self.handle.RAMEnabled = True
        self.handle.GPUEnabled = True
        self.handle.HDDEnabled = True
        self.handle.Open()
        # Holds hardware objects, keys are the IDs (ex: /hdd/0), holds the objects as the values
        self.hardware_obj_dict = {}
        # Holds the sensor IDs of the values we want easy access to, so it doesnt need to be iteratively found every time the value is needed
        self.key_values = {"GT":None,   # Gpu temp
                           "GL":None,   # Gpu load
                           "CT":None,   # Cpu temp
                           "CL":None,   # Cpu load
                           "RL":None}   # Ram load
        print("Initializing OHM Reading")
        # Iterate over each hardware component (cpu, gpu, ram, etc)
        for hardware_item in self.handle.Hardware:
            # OHM side of things, update the values
            hardware_item.Update()
            # Create new hardware object
            hardware_obj = OHardware(hardware_item.Identifier, hardware_item.Name, hardware_item.HardwareType, hardware_item.Parent)
            # Iterate over each hardware sensor (temperature, clock, load, etc)
            for sensor_item in hardware_item.Sensors:
                if sensor_item.Value is not None: # Duh
                    # Create the sensor object (something like CPU Core 1 Temperature)
                    new_sensor = OSensor(sensor_item.Name,sensor_item.SensorType,sensor_item.Value,sensor_item.Index, sensor_item.Identifier)
                    # Add sensor object to hardware object
                    hardware_obj.add_sensor(str(sensor_item.SensorType), new_sensor)
            # Add hardware object to be tracked
            self.hardware_obj_dict[hardware_obj.id] = hardware_obj
        print("Initialization Auto-Relationship Finder")
        # Now that all hardware & sensors are added, we can track the important values
        self.isolate_key_values()
        end_init = time.time()
        print("Initialization of Hardware Sensors Completed. Elapsed: {t:4.2}s".format(t=end_init-start_init))

    # Refreshes hardware sensor values and update them in stored objects
    # Params: self (duh)
    # Returns: N/A
    def read(self):
        # Iterate over each hardware component
        for hardware_item in self.handle.Hardware:
            # Update values
            hardware_item.Update()
            # Get the object that corresponds to the component we're iterating over
            hardware_obj = self.hardware_obj_dict[str(hardware_item.Identifier)]
            # Iterate over hardware COMPONENT sensors (NOT THE OBJECT YET)
            for sensor_item in hardware_item.Sensors:
                if sensor_item.Value is not None: # Try to keep up
                    # Store sensor COMPONENT value into sensor object
                    hardware_obj.sens_ids[str(sensor_item.Identifier)].log(sensor_item.Value)

    # Finds the ID's of the important sensors that are wanted
    # Params: self (duh)
    # Returns: N/A
    def isolate_key_values(self):
        # Iterate over each hardware object
        for hardware_id, hardware_obj in self.hardware_obj_dict.items():
            # Need cpu, ram and gpu
            match hardware_obj.type:
                case 'CPU':
                    # Iterate over sensor objects by type, looking for temperature and load sensors
                    for id, sensor_obj in hardware_obj.sens_ids.items():
                        match sensor_obj.type:
                            case 'Temperature':
                                # This may need adjusting - but CPU Package is the 'general' cpu temp sensor
                                if sensor_obj.name == "CPU Package":
                                    self.key_values["CT"] = (hardware_id, id)
                            case 'Load':
                                if sensor_obj.name == "CPU Total":
                                    self.key_values["CL"] = (hardware_id, id)
                            case _:
                                pass
                case 'RAM':
                    for id, sensor_obj in hardware_obj.sens_ids.items():
                        match sensor_obj.type:
                            case 'Load':
                                self.key_values["RL"] = (hardware_id, id)
                case 'GpuNvidia' | 'GpuAti':
                    for id, sensor_obj in hardware_obj.sens_ids.items():
                        match sensor_obj.type:
                            case 'Temperature':
                                if sensor_obj.name == "GPU Core":
                                    self.key_values["GT"] = (hardware_id, id)
                            case 'Load':
                                if sensor_obj.name == "GPU Core":
                                    self.key_values["GL"] = (hardware_id, id)
                            case _:
                                pass                    
                case _:
                    pass
        # Now check we got everything            
        for codename, id in self.key_values.items():
            if id is not None:
                print("\tConnected: {c} -> [{i}]{j}".format(c=codename, i=id[0], j=id[1]))
            else:
                print("\tFailed: {c}".format(c=codename))
    def get_values_to_send(self):
        retval = []
        for key in ['CT','GT','RL','CL','GL']:
            average = self.hardware_obj_dict[self.key_values[key][0]].sens_ids[self.key_values[key][1]].history.get_avg()
            retval.append(round(average))
        return retval
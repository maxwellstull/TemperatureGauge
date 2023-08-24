
import time
import clr
clr.AddReference(r'OpenHardwareMonitorLib')
from OpenHardwareMonitor import Hardware 

from classes import OHardware, OSensor, CQueue
class hardwareLogger():
    def __init__(self):
        start_init = time.time()
        print("Initializing OHM Connection")
        self.handle = Hardware.Computer()
        self.handle.MainboardEnabled = True
        self.handle.CPUEnabled = True
        self.handle.RAMEnabled = True
        self.handle.GPUEnabled = True
        self.handle.HDDEnabled = True
        self.handle.Open()

        self.hardware_obj_dict = {}

        self.key_values = {"GT":None,
                           "GL":None,
                           "CT":None,
                           "CL":None,
                           "RL":None}
        print("Initializing OHM Reading")
        for hardware_item in self.handle.Hardware: # Iterate over each hardware component (CPU, GPU, RAM)
            hardware_item.Update() # Gets updated values
            hardware_obj = OHardware(hardware_item.Identifier, hardware_item.Name, hardware_item.HardwareType, hardware_item.Parent) # Create hardware object
            for sensor_item in hardware_item.Sensors: # Iterate over each hardware sensor (temperature, clock, load)
                if sensor_item.Value is not None: # Duh
                    # Create the sensor object (something like CPU Core 1 Temperature)
                    new_sensor = OSensor(sensor_item.Name,sensor_item.SensorType,sensor_item.Value,sensor_item.Index, sensor_item.Identifier)
                    hardware_obj.add_sensor(str(sensor_item.SensorType), new_sensor)
            self.hardware_obj_dict[hardware_obj.id] = hardware_obj
        print("Initialization Auto-Relationship Finder")
        self.isolate_key_values()
        
        end_init = time.time()
        print("Initialization of Hardware Sensors Completed. Elapsed: {t:4.2}s".format(t=end_init-start_init))
    
    def read(self):
        for hardware_item in self.handle.Hardware:
            hardware_item.Update()
            hardware_obj = self.hardware_obj_dict[str(hardware_item.Identifier)]
            for sensor_item in hardware_item.Sensors:
                if sensor_item.Value is not None:
                    try:
                        hardware_obj.sens_ids[str(sensor_item.Identifier)].log(sensor_item.Value)
                    except:
                        print("Failed ", sensor_item.Value, type(sensor_item.Value))
    # We want GPU temp & load, CPU temp & load, and RAM load
    def isolate_key_values(self):
        for key, hardware_obj in self.hardware_obj_dict.items():
            match hardware_obj.type:
                case 'CPU':
                    for id, sensor_obj in hardware_obj.sens_ids.items():
                        match sensor_obj.type:
                            case 'Temperature':
                                if sensor_obj.name == "CPU Package":
                                    self.key_values["CT"] = id
                            case 'Load':
                                if sensor_obj.name == "CPU Total":
                                    self.key_values["CL"] = id
                            case _:
                                pass
                case 'RAM':
                    for id, sensor_obj in hardware_obj.sens_ids.items():
                        match sensor_obj.type:
                            case 'Load':
                                self.key_values["RL"] = id
                case 'GpuNvidia' | 'GpuAti':
                    for id, sensor_obj in hardware_obj.sens_ids.items():
                        match sensor_obj.type:
                            case 'Temperature':
                                if sensor_obj.name == "GPU Core":
                                    self.key_values["GT"] = id
                            case 'Load':
                                if sensor_obj.name == "GPU Core":
                                    self.key_values["GL"] = id
                            case _:
                                pass                    
                case _:
                    pass
        # Now check we got everything            
        for codename, id in self.key_values.items():
            print("\tConnected: {c} -> {i}".format(c=codename, i=id))
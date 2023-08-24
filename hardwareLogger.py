
import time
import clr
clr.AddReference(r'OpenHardwareMonitorLib')
from OpenHardwareMonitor import Hardware 

from classes import OHardware, OSensor, CQueue
class hardwareLogger():
    def __init__(self):
        start_init = time.time()

        self.handle = Hardware.Computer()
        self.handle.MainboardEnabled = True
        self.handle.CPUEnabled = True
        self.handle.RAMEnabled = True
        self.handle.GPUEnabled = True
        self.handle.HDDEnabled = True
        self.handle.Open()

        self.hardware_obj_dict = {}

        for hardware_item in self.handle.Hardware: # Iterate over each hardware component (CPU, GPU, RAM)
            hardware_item.Update() # Gets updated values
            hardware_obj = OHardware(hardware_item.Identifier, hardware_item.Name, hardware_item.HardwareType, hardware_item.Parent) # Create hardware object
            for sensor_item in hardware_item.Sensors: # Iterate over each hardware sensor (temperature, clock, load)
                if sensor_item.Value is not None: # Duh
                    # Create the sensor object (something like CPU Core 1 Temperature)
                    new_sensor = OSensor(sensor_item.Name,sensor_item.SensorType,sensor_item.Value,sensor_item.Index, sensor_item.Identifier)
                    hardware_obj.add_sensor(str(sensor_item.SensorType), new_sensor)
            self.hardware_obj_dict[hardware_item.Identifier] = hardware_obj
        end_init = time.time()
        print("Initialization of Hardware Sensors Completed. Elapsed: {t:4.2}s".format(t=end_init-start_init))
    
    def read(self):
        for hardware_item in self.handle.Hardware:
            hardware_item.Update()
            hardware_obj = self.hardware_obj_dict[hardware_item.Identifier]
            for sensor_item in hardware_item.Sensors:
                if sensor_item.Value is not None:
                    hardware_obj.sens_ids[sensor_item.Identifier].log(sensor_item.Value)


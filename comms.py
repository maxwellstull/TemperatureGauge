#import serial
#ser = serial.Serial('COM6',9600)
#print(ser.name)
#ser.write(b'50')
#s = ser.read()
#print(s)


#import serial
#import time
#arduino = serial.Serial(port='COM6', baudrate=115200, timeout=.1)
#def write_read(x):
#    arduino.write(bytes(x, 'utf-8'))
#    time.sleep(0.05)
#    data = arduino.readline()
#    return data
#while True:
#    num = input("Enter a number: ") # Taking input from user
#    value = write_read(num)
#    print(value) # printing the value
openhardwaremonitor_hwtypes = ['Mainboard','SuperIO','CPU','RAM','GpuNvidia','GpuAti','TBalancer','Heatmaster','HDD']
openhardwaremonitor_sensortypes = ['Voltage','Clock','Temperature','Load','Fan','Flow','Control','Level','Factor','Power','Data','SmallData','Throughput']
import os 
import clr
import time
clr.AddReference(r'OpenHardwareMonitorLib')

from OpenHardwareMonitor import Hardware
handle = Hardware.Computer()
handle.MainboardEnabled = True
handle.CPUEnabled = True
handle.RAMEnabled = True
handle.GPUEnabled = True
handle.HDDEnabled = True
handle.Open()


dicty = {}
from classes import OHardware, OSensor, CQueue
## once
for i in handle.Hardware: # Iterate over each hardware component (CPU, GPU, RAM)
    i.Update() # Gets updated values
    new_hw = OHardware(i.Identifier, i.Name, i.HardwareType, i.Parent) # Create hardware object
    print(new_hw)    
    for sensor in i.Sensors: # Iterate over each hardware sensor (temperature, clock, load)
        if sensor.Value is not None: # Duh
            # Create the sensor object (something like CPU Core 1 Temperature)
            new_sensor = OSensor(sensor.Name,sensor.SensorType,sensor.Value,sensor.Index, sensor.Identifier)
            new_hw.add_sensor(str(sensor.SensorType), new_sensor)
    dicty[i.Identifier] = new_hw

for _ in range(0,10): # Loop to read
    time.sleep(0.1) # Leave a gap
    for i in handle.Hardware:
        i.Update()
        recalled = dicty[i.Identifier]

        for sensor in i.Sensors:
            if sensor.Value is not None:
                recalled.sens_ids[sensor.Identifier].log(sensor.Value)

for key, value in dicty.items():
    print(value.short())

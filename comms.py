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
import time
from hardwareLogger import hardwareLogger

hw = hardwareLogger()

for _ in range(0,60): # Loop to read
    time.sleep(0.5)
    start = time.time()
    hw.read()
    end = time.time()
    print("Read duration: {t:4.4}s".format(t=end-start))

for key, value in hw.hardware_obj_dict.items():
    print(value.short())

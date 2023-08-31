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

REFRESH_RATE_HZ = 0.5


import time
import asyncio
import serial
from hardwareLogger import hardwareLogger
from serialComm import serialComm
import serial.tools.list_ports

async def main():
    ports = serial.tools.list_ports.comports()
    portname = ""
    for port in ports:
        if 'Arduino' in port[1]:
            portname = port[0]

    refresh_period_sec = 1/REFRESH_RATE_HZ
    hw = hardwareLogger()
    arduino = serialComm(port=portname, baud=115200, timeout=0.1)
    print(arduino.write_read('12'))
    for _ in range(0,10): # Loop to read
        start = time.time()
        hw.read()





        await asyncio.sleep(refresh_period_sec - (time.time() - start))


    for key, value in hw.hardware_obj_dict.items():
        print(value)


if __name__ == "__main__":
    asyncio.run(main())
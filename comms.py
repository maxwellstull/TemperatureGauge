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

READ_REFRESH_RATE_HZ = 4
SEND_REFRESH_RATE_HZ = 0.5


import time
import asyncio
import serial
from hardwareLogger import hardwareLogger
from serialComm import serialComm
import serial.tools.list_ports



async def read_coroutine(hw):
    period = 1/READ_REFRESH_RATE_HZ
    while(True):
        start = time.time()
        hw.read()
        print("[RC] Values updated", time.time())
        await asyncio.sleep(period - (time.time() - start))

async def send_coroutine(hw):
    period = 1/SEND_REFRESH_RATE_HZ
    found_port = False
    portname = ""
    ctr = 0
    while(found_port is False):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if 'Arduino' in port[1]:
                print("[SC] Arduino port identified: ", port[0])
                portname = port[0]
                found_port = True
        await asyncio.sleep(1)
        if ctr % 5 == 0:
            print("[SC] Attempting to identify to Arduino port", time.time())
        ctr += 1
    arduino = serialComm(port=portname, baud=9600, timeout=1)
    while(True):
        start = time.time()
        to_send = hw.get_values_to_send()
        to_send_str = "{:3}{:3}{:3}{:3}{:3}".format(to_send[0], to_send[1], to_send[2], to_send[3], to_send[4])
        print("[SC] Sending", to_send, " ", time.time())
        result = arduino.write_read(to_send_str)
        if(result == b'1'):
            pass 
        else:
            print("[SC] Ak not received", time.time())
        await asyncio.sleep(period - (time.time() - start))

async def main():
    hw = hardwareLogger()
    await asyncio.gather(read_coroutine(hw), send_coroutine(hw))

if __name__ == "__main__":
    asyncio.run(main())
    
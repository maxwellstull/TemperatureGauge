
import serial
import time

class serialComm():
    def __init__(self, port='COM6',baud=115200,timeout=0.1):
        self.arduino = serial.Serial(port=port, baudrate=baud, timeout=timeout)
    def write_read(self, x):
        self.arduino.write(bytes(x, 'utf-8'))
        time.sleep(0.05)
        data = self.arduino.readline()
        return data
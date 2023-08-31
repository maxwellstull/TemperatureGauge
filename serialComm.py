
import serial
import time

class serialComm():
    def __init__(self, port='COM6',baud=9600,timeout=0.5):
        self.arduino = serial.Serial(port=port, baudrate=baud, timeout=timeout)
    def write_read(self, x):
        self.arduino.write(bytes(x, 'utf-8'))
        data = self.arduino.read(100)
        return data
    def write(self, x):
        self.arduino.write(bytes(x, 'utf-8'))
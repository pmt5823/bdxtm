import serial
import time

arduino = serial.Serial('COM3',9600,timeout=1)
time.sleep(2)

def open_barrier():
    arduino.write(b'OPEN\n')
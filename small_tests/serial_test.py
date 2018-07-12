import serial
import time

arduino = serial.Serial('COM5', 9600)
d das
while True:
    arduino.write(b'1')
    time.sleep(1)
    arduino.write(b'0')
    time.sleep(1)

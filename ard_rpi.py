import serial
import time
port = "/dev/ttyUSB0"

serialFromArduino=serial.Serial(port,9600)
time.sleep(1)
serialFromArduino.flushInput()
string1='<dis>HI'
serialFromArduino.write(string1.encode())
while True:
    if(serialFromArduino.inWaiting()>0):
        input=serialFromArduino.readline()
        print(input)
import pyfirmata
from time import sleep
board=pyfirmata.Arduino('/dev/ttyUSB0')
pin=board.get_pin('d:13:0')
it=pyfirmata.util.Iterator(board)
it.start()


import RPi.GPIO as GPIO
import time
import serial
import pyfirmata
from time import sleep
GPIO.setmode(GPIO.BCM)

servo_pins=[4,2]#servo_setting
servo_pwms=[]
for servo_pin in servo_pins:
    GPIO.setup(servo_pin,GPIO.OUT)
    servo_pwms.append(GPIO.PWM(servo_pin,100))
for servo_pwm in servo_pwms:
    servo_pwm.start(5)
def turntoangle(servo_pwms,angle):
    duty=float(angle)/180.*20+5
    for servo_p in servo_pwms:
        servo_p.ChangeDutyCycle(duty)
SEQUENCE = [[GPIO.HIGH,GPIO.HIGH,GPIO.LOW,GPIO.LOW], #stepping_setting
            [GPIO.LOW,GPIO.HIGH,GPIO.HIGH,GPIO.LOW],
            [GPIO.LOW,GPIO.LOW,GPIO.HIGH,GPIO.HIGH],
            [GPIO.HIGH,GPIO.LOW,GPIO.LOW,GPIO.HIGH,]]

STEPPER_PINS = [26,19,13,6]
for pin in STEPPER_PINS:
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
SEQUENCE_COUNT = len(SEQUENCE)
def stepper_step(stepper_pins,steps,direction):
    step=0
    steps=steps*576
    sequence_index = 0
    PINS_COUNT = len(STEPPER_PINS)
    while step<steps:
        sequence_index += direction
        sequence_index %= SEQUENCE_COUNT
        if step<steps:
            for pin in range(0, PINS_COUNT):
                 GPIO.output(stepper_pins[pin], SEQUENCE[sequence_index][pin])
        step+=1
        time.sleep(0.003)

port = "/dev/ttyUSB0"
serialFromArduino=serial.Serial(port,9600)
serialFromArduino.flushInput()
time.sleep(0.5)
'''
while True:
    board=pyfirmata.Arduino('/dev/ttyUSB0')
pin=board.get_pin('d:13:0')
it=pyfirmata.util.Iterator(board)
it.start()
'''

import select
import socket
import struct
import sys
import os
import numpy as np
import cv2 as cv
import signal

def recvAll(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def send_msg(sock, msg):
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def recv_msg(sock):
    raw_msglen = recvAll(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    return recvAll(sock, msglen)

def imageToBytes(img):
    img_str = cv.imencode('.jpg', img)[1].tostring()
    return img_str

from picamera.array import PiRGBArray
from picamera import PiCamera
cam = PiCamera(resolution=(1920, 1088))
rawCapture = PiRGBArray(cam)

#s = socket.socket()
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#port = 12349
#s.bind(('', port))

#s.listen(5)

#c, addr = s.accept()
#print('Got connection from', addr)

def placebook(place):
    if place==5:
        return
    stepper_step(STEPPER_PINS,10*place,1)
    serialFromArduino.flushInput()
    time.sleep(0.5)
    command='<push>R'
    serialFromArduino.write(command.encode())
    time.sleep(3.5)
    command='<push>L'
    time.sleep(2)
    serialFromArduino.write(command.encode())
    stepper_step(STEPPER_PINS,10*place,-1)
def getplace(book_text):
    return 1
try:    
    while True:
        while True:
            if(serialFromArduino.inWaiting()>0):
                message=serialFromArduino.readline()
                if message==b'<book>\n':
                    break
                message=" "
       # command = ''
        #command = '<dis>Book has detected! delivering to slot '
        book_state=serialFromArduino.readline()
        book_state=book_state.decode()
        place=5
        for i in range(0,4):
           # print(book_state)
            if book_state[i+8]=='0':
                place=i
                break
        '''if place == 5:
            command = 'No slot left!'
        else:
            command = command + str(place+1)
        serialFromArduino.write(command.encode())
        command = '<DATA>'
        for i in range(0,4):
            if book_state[i+8]=='1':
                if command == '<DATA>':
                    command = '<DATA>A book in slot '
                    command = command + str(i+1)
                else:
                    command = command + ';A book in slot ' + str(i+1)
        serialFromArduino.write(command.encode())
        '''
        '''
        arrived = False
        while not arrived:
            cam.capture(rawCapture, format='bgr')
            camImage = rawCapture.array
            send_msg(c, b'OCR')
            send_msg(c, imageToBytes(camImage))
            text = recv_msg(c).decode()
            send_msg(c, b'saveLast')
            arrived = True
            rawCapture.truncate(0)
            time.sleep(0.5)
        #place=getplace(text)
        '''
        
        print(place)
        #time.sleep(0.5)
        #turntoangle(servo_pwms,180)
        #time.sleep(0.5)
        #stepper_step(STEPPER_PINS,5,-1)
        placebook(place)
        time.sleep(1)
finally:
    GPIO.cleanup()
    #cam.release()

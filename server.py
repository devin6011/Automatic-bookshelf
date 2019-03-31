import select
import socket
import struct
import sys
import os
import numpy as np
import cv2 as cv
import signal

socketList = []

def intHandler(sig, frame):
    print('Bye')
    for s in socketList:
        s.close()
    sys.exit(0)

signal.signal(signal.SIGINT, intHandler)

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

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socketList.append(s)
port = 12349
s.bind(('', port))

s.listen(5)

while True:
    c, addr = s.accept()
    socketList.append(c)
    print('Got connection from', addr)
    while True:
        rlist, wlist, xlist = select.select([sys.stdin, c], [], [])
        cam.capture(rawCapture, format='bgr')
        camImage = rawCapture.array
        for f in rlist:
            if f is c:
                pass
            elif f is sys.stdin:
                cmd = sys.stdin.readline().strip()
                if cmd == 'OCR':
                    send_msg(c, b'OCR')
                    send_msg(c, imageToBytes(camImage))
                    text = recv_msg(c).decode()
                    print(text)
                elif cmd == 'saveLast':
                    send_msg(c, b'saveLast')
                elif cmd == 'getOrdering':
                    send_msg(c, b'getOrdering')
                    order = recv_msg(c).decode().split(',')
                    print(order)
                elif cmd == 'OCRsegment':
                    send_msg(c, b'OCRsegment')
                    send_msg(c, imageToBytes(camImage))
                    text = recv_msg(c).decode()
                    print(text)
                elif cmd == 'transferImage':
                    send_msg(c, b'transferImage')
                    send_msg(c, imageToBytes(camImage))
                    filename = recv_msg(c).decode()
                    print(filename)
                elif cmd == 'exit':
                    print('Bye')
                    c.close()
                    s.close()
                    sys.exit(0)
                else:
                    print('Error: bad command.')
                pass
            else:
                print('Error: bad file descriptor.')
        rawCapture.truncate(0)

    c.close()
s.close()

cv.release()
cv.destroyAllWindows()

import socket
import select
from imageGod import *
import numpy as np
import cv2 as cv
import struct
import uuid
import os
import sys

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

def toImage(data):
    nparr = np.frombuffer(data, np.uint8)
    img = cv.imdecode(nparr, cv.IMREAD_COLOR)
    return img

for filename in os.listdir('database'):
    filepath = os.path.join('database', filename)
    try:
        if os.path.isfile(filepath):
            os.unlink(filepath)
    except Exception as e:
        print(e)

fileCount = 0

s = socket.socket()
host = '10.20.2.236'
port = 12349

s.connect((host, port))
print('Connect to %s:%s successful' % (host, port))
while True:
    rlist, wlist, xlist = select.select([sys.stdin, s], [], [])
    for f in rlist:
        if f is s:
            cmd = recv_msg(s)
            if cmd is None:
                print('The server is down')
                s.close()
                sys.exit(0)
            cmd = cmd.decode()
            if cmd == 'OCR':
                img = toImage(recv_msg(s))
                result = OCR(img)
                send_msg(s, result.encode())
            elif cmd == 'saveLast':
                ocr = OCR(img)
                ocrSeg = textSegment(ocr)
                fileCount += 1
                filename = str(fileCount)
                cv.imwrite('database/' + filename + '.jpg', img)
                with open('database/' + filename + '.txt', 'w') as f:
                    f.write(ocr)
                with open('database/' + filename + '.seg', 'w') as f:
                    f.write(ocrSeg)
                #send_msg(s, filename.encode())
            elif cmd == 'textSegment':
                data = recv_msg(s).decode()
                result = textSegment(data)
                send_msg(s, result.encode())
            elif cmd == 'OCRsegment':
                img = toImage(recv_msg(s))
                result = textSegment(OCR(img))
                send_msg(s, result.encode())
            elif cmd == 'extractFeature':
                data = recv_msg(s).decode()
                result = ','.join(extractFeature(data))
                send_msg(s, result.encode())
            elif cmd == 'featureMatching':
                img1 = toImage(recv_msg(s))
                img2 = toImage(recv_msg(s))
                result = str(featureMatching(img1, img2))
                send.msg(s, result.encode())
            elif cmd == 'search':
                pattern = recv_msg(s).decode()
                fileList = os.listdir('database')
                matches = []
                textList = filter(lambda x : x.split('.')[-1] == 'txt', fileList)
                for filename in textList:
                    with open('database/' + filename, 'r') as f:
                        text = f.read()
                        if pattern in text:
                            matches.append(filename.split('.')[:-1])
                matches = ','.join(matches)
                send.msg(s, matches.encode())
            elif cmd == 'transferImage':
                img = toImage(recv_msg(s))
                ocr = OCR(img)
                ocrSeg = textSegment(ocr)
                filename = str(uuid.uuid4())
                cv.imwrite('database/' + filename + '.jpg', img)
                with open('database/' + filename + '.txt', 'w') as f:
                    f.write(ocr)
                with open('database/' + filename + '.seg', 'w') as f:
                    f.write(ocrSeg)
                send_msg(s, filename.encode())
            elif cmd == 'doClustering':
                fileList = os.listdir('database')
                corpora = []
                segList = filter(lambda x : x.split('.')[-1] == 'seg', fileList)
                for filename in segList:
                    with open('database/' + filename, 'r') as f:
                        corpus = f.read()
                        corpora.append(corpus)
                result = ','.join(topicClustering(corpus))
                send.msg(s, result.encode())
            elif cmd == 'getOrdering':
                fileList = os.listdir('database')
                corpora = []
                segList = list(filter(lambda x : x.split('.')[-1] == 'seg', fileList))
                segList.sort(key = lambda x : int(x.split('.')[0]))
                for filename in segList:
                    with open('database/' + filename, 'r') as f:
                        corpus = f.read()
                        corpora.append(corpus)
                labels = topicClustering(corpora)
                order = [i for i in range(len(labels))]
                order.sort(key = lambda x : labels[x])
                order = [i+1 for i in order]
                result = ','.join(order)
                send.msg(s, result.encode())
            else:
                send_msg(s, 'Incorrect Command! I AM ANGRY!'.encode())
        elif f is sys.stdin:
            cmd = sys.stdin.readline().strip()
            if cmd == '':
                pass
            elif cmd == '':
                pass
            elif cmd == 'exit':
                print('Bye')
                s.close()
                sys.exit(0)
            else:
                print('Error: bad command.')
        else:
            print('Error: bad file descriptor.')

s.close()

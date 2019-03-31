import RPi.GPIO as GPIO
import time
import cv2
cam=cv2.VideoCapture(0)
if not cam.isOpend():
    raise IOError("cannot open cam")
while True:
    ret,frame=cam.read()
    cv2.show('frame',frame)
cv2.release()
cv2.destoryAllWindows()

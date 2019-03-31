import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
step_pin=2
dir_pin=3
GPIO.setup(step_pin,GPIO.OUT)
GPIO.setup(dir_pin,GPIO.OUT)
#p=GPIO.PWM(step_pin,200)
#p.start(1)
try:
    while True:
         GPIO.output(dir_pin,GPIO.HIGH)
    # GPIO.output(step_pin,GPIO.HIGH)
    #p.start(1)
        time.sleep(0.05)
    #p.stop()
        time.sleep(0.05)
        #time.sleep(0.05)
finally:
    GPIO.cleanup()

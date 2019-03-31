import Rpi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
led_pin=4
GPIO.setup(led_pin,GPIO.OUT)
GPIO.output(led_pin,GPIO.LOW)
try:
    while True:
        GPIO.output(led_pin,GPIO.HIGH)
        time.sleep(1)
        GPIO.output(led_pin,GPIO.LOW)
finally:
    GPIO.cleanup()

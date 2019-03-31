import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
servo_pins=[4,2]

servo_ps=[]
for servo_pin in servo_pins:
    GPIO.setup(servo_pin,GPIO.OUT)
    servo_ps.append(GPIO.PWM(servo_pin,100))
for servo_p in servo_ps:
    servo_p.start(5)
def turntoangle(servo_ps,angle):
    duty=float(angle)/180.*20+5
    for servo_p in servo_ps:
        servo_p.ChangeDutyCycle(duty)
        print(duty)
try:
    while True:
        #angle=input('please input')
        turntoangle(servo_ps,0)
        time.sleep(1)
        turntoangle(servo_ps,180)
        time.sleep(1)
finally:
    GPIO.cleanup()
        


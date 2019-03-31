import sys
import time
import RPi.GPIO as GPIO
 
GPIO.setmode(GPIO.BCM)
 
STEPS_PER_REVOLUTION = 32 * 64
SEQUENCE = [[GPIO.HIGH,GPIO.HIGH,GPIO.LOW,GPIO.LOW],
            [GPIO.LOW,GPIO.HIGH,GPIO.HIGH,GPIO.LOW],
            [GPIO.LOW,GPIO.LOW,GPIO.HIGH,GPIO.HIGH],
            [GPIO.HIGH,GPIO.LOW,GPIO.LOW,GPIO.HIGH,]]
 
STEPPER_PINS = [26,19,13,6]
for pin in STEPPER_PINS:
  GPIO.setup(pin,GPIO.OUT)
  GPIO.output(pin, GPIO.LOW)
 
SEQUENCE_COUNT = len(SEQUENCE)
 
direction = 1
steps = 0
def stepper_step(stepper_pins,steps,direction):
    step=0
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
try:
    while True:
        stepper_step(STEPPER_PINS,576,1)
        time.sleep(0.5)
        stepper_step(STEPPER_PINS,576,-1)
finally:
    GPIO.cleanup()

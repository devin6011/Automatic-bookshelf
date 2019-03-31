import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
 
STEPS_PER_REVOLUTION = 64 * 64
SEQUENCE = [[1,0,0,0],
            [1,1,0,0],
            [0,1,0,0],
            [0,1,1,0],
            [0,0,1,0],
            [0,0,1,1],
            [0,0,0,1],
            [1,0,0,1]]
 
STEPPER_PINS = [26,19,13,6]
for pin in STEPPER_PINS:
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
 
SEQUENCE_COUNT = len(SEQUENCE)
PINS_COUNT = len(STEPPER_PINS)
sequence_index = 0
direction = 1
wait_time = 1/float(1000)
def stepper(stepper_pins,steps):
    step=0
    sequence_index += direction
    sequence_index %= SEQUENCE_COUNT
    if step<steps:
        for pin in range(0, PINS_COUNT):
            GPIO.output(STEPPER_PINS[pin], SEQUENCE[sequence_index][pin])
    step+=1
    time.sleep(wait_time)
try:
    while True:
        for pin in range(0, PINS_COUNT):
            GPIO.output(STEPPER_PINS[pin], SEQUENCE[sequence_index][pin])
            
 
        steps += direction
        if steps >= STEPS_PER_REVOLUTION:
            direction = -1
        elif steps < 0:
            direction = 1
 
        sequence_index += direction
        sequence_index %= SEQUENCE_COUNT
        time.sleep(wait_time)
        print(wait_time)
except KeyboardInterrupt:
    print('關閉程式')
finally:
    GPIO.cleanup()

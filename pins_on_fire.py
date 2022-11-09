import RPi.GPIO as gpio
from time import sleep

gpio.setmode(gpio.BCM)
gpio.setup(14, gpio.OUT)

food_dispenser_servo = gpio.PWM(14,50)

duty = 5
x = 0

try:
    while True:
        food_dispenser_servo.start(0)
        sleep(0.5)
        if x < 20:
            food_dispenser_servo.ChangeDutyCycle(duty)
        else:
            break
            print("loop broke")

            
        
except KeyboardInterrupt:
    print("programme stopped")

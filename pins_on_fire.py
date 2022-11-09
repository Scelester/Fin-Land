import RPi.GPIO as gpio
from time import sleep

gpio.setmode(gpio.BCM)
gpio.setup(14, gpio.OUT)

food_dispenser_servo = gpio.PWM(14,50)

try:
    while True:
        food_dispenser_servo.start(0)
        
        # wait 2 seconds 
        sleep(1)

        duty = 2
        while duty <= 17:
            food_dispenser_servo.ChangeDutyCycle(duty)
            sleep(1)
            duty += 1
        
except KeyboardInterrupt:
    print("programme stopped")

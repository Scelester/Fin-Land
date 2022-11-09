import RPi.GPIO as gpio
from time import sleep

gpio.setwarnings(False)

gpio.setmode(gpio.BCM)
gpio.setup(14, gpio.OUT)

food_dispenser_servo = gpio.PWM(14,50)

duty = 1

try:
    while True:
        print("11111111111111111111111111111")
        food_dispenser_servo.start(0)
        sleep(0.5)
        
        while duty < 20:
            print("2222222222222222222222")
            food_dispenser_servo.ChangeDutyCycle(duty)
            duty += 1
            sleep(1)


        print("loop broke")

except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
   print("Keyboard interrupt")

except:
   print("some error") 

finally:
   print("clean up") 
   gpio.cleanup() # cleanup all GPIO 
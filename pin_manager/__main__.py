import RPi.GPIO as gpio
from time import sleep

# importing files
from food_servo import start_servo


gpio.setmode(gpio.BCM)
gpio.setup(14, gpio.OUT)

food_dispenser_servo = gpio.PWM(14,50)

duty = 1

try:
    while True:
      print("aaaaaaaaaaaa")
      start_servo(food_dispenser_servo, duty)
      print("ok")

except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
   print("Keyboard interrupt")

except:
   print("some error") 

finally:
   print("clean up") 
   gpio.cleanup() # cleanup all GPIO 
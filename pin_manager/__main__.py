import RPi.GPIO as gpio
from time import sleep

# importing files
from food_servo import start_servo

# setting up goio keys
gpio.setmode(gpio.BCM)


# servo motor setup
gpio.setup(14, gpio.OUT) # output signal fo GPIO
food_dispenser_servo = gpio.PWM(14,50)    # setting frequency
servo_initial_duty = 1
STATE_SERVO = True



try:
    while True:
      if STATE_SERVO:
         start_servo(food_dispenser_servo, servo_initial_duty)
      
      STATE_SERVO = False

except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
   print("Keyboard interrupt")

except:
   print("some error") 

finally:
   print("clean up") 
   gpio.cleanup() # cleanup all GPIO 
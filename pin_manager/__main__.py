import RPi.GPIO as gpio
from time import sleep

# importing files
from food_servo import start_servo

# setting up goio keys
gpio.setmode(gpio.BCM)


# --------------------------------- Outputs --------------------------------

# servo motor setup
gpio.setup(14, gpio.OUT) # output signal fo GPIO
food_dispenser_servo = gpio.PWM(14,50)    # setting frequency
servo_initial_duty = 1
food_timer = 5
STATE_SERVO = False





# --------------------------------- Inputs --------------------------------

# pH sensor setup
gpio.setup(23,gpio.IN)




try:
    while True:
      if STATE_SERVO:
         start_servo(food_dispenser_servo, servo_initial_duty)
      
      for n in range(14):
         print(n,". Ph input :",gpio.input(23))

      # delay so that raspberri-pi doesn't freezes



except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
   print("Keyboard interrupt")

except:
   print("some error") 

finally:
   print("clean up") 
   gpio.cleanup() # cleanup all GPIO 
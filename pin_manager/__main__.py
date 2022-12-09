import RPi.GPIO as gpio
from time import sleep
from time import perf_counter as clock

# importing files
from food_servo import start_servo
from Dphsense import get_ph_value
from relay_me import relay_module
import supabase_manager

# setting up goio keys
gpio.setmode(gpio.BCM)

# servo motor setup
gpio.setup(14, gpio.OUT) # output signal fo GPIO
food_dispenser_servo = gpio.PWM(14,50)    # setting frequency
servo_initial_duty = 1
food_timer = 5
STATE_SERVO = True


# --------------------------- Clock setup ---------------------------------
initial_timer = clock()



# --------------------------- Relay stuff ------------------------------------
relay_pin1 = 16
gpio.setup(relay_pin1,gpio.OUT)
STATE_RELAY1 = False
STATE_RELAY2 = False
STATE_RELAY3 = False
STATE_RELAY4 = False

# --------------------------------- Inputs --------------------------------

# pH sensor setup
gpio.setup(23,gpio.IN)
# gpio.setup(14,gpio.IN)



try:
    while True:
      if STATE_SERVO:
         start_servo(food_dispenser_servo, servo_initial_duty)
      
      supabase_manager.send_ph_value_to_database(
          get_ph_value()
        )

      # print(gpio.input(14))

      # relay stuff
      if STATE_RELAY1:
        relay_module(relay_pin1)
      elif STATE_RELAY2:
        pass
      elif STATE_RELAY3 or STATE_RELAY4:
        pass
            
      
      if clock() - initial_timer >= 50:
        break

      # delay some time
      sleep(1)


except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
   print("Keyboard interrupt")


# other errors
except:
   print("some error") 


finally:
   print("clean up") 
   gpio.cleanup() # cleanup all GPIO 

import RPi.GPIO as gpio
from time import sleep
from time import perf_counter as clock

# importing files
from food_servo import start_servo
from Dphsense import get_ph_value
import supabase_manager
import asyncio
import datetime

# setting up goio keys
gpio.setmode(gpio.BCM)

# servo motor setup
gpio.setup(14, gpio.OUT) # output signal fo GPIO
food_dispenser_servo = gpio.PWM(14,50)    # setting frequency
servo_initial_duty = 1
food_timer = 5
STATE_SERVO = False

#----------------------------- Date & time sets -------------------------------------
datetx = datetime.datetime.now()
print(str(datetx.hour)+"."+str(datetx.minute))


# --------------------------- Clock setup ---------------------------------
initial_timer = clock()



# --------------------------- Relay stuff ------------------------------------
relay_pin1 = 16
relay_pin2 = 20
relay_pin3 = 21
relay_pin4 = 26
gpio.setup(relay_pin1,gpio.OUT)
gpio.setup(relay_pin2,gpio.OUT)
gpio.setup(relay_pin3,gpio.OUT)
gpio.setup(relay_pin4,gpio.OUT)
STATE_RELAY1 = False
STATE_RELAY2 = False
STATE_RELAY3 = False


relay_list = [relay_pin1, relay_pin2, relay_pin3, relay_pin4]

# --------------------------------- Inputs --------------------------------

# Temp sensor setup
temppin = 23
gpio.setup(temppin,gpio.IN)
def tempdata(pin=temppin):
  return gpio.input(pin)


inputer_sender_lopper = 0

try:
    while True:
      if STATE_SERVO:
         start_servo(food_dispenser_servo, servo_initial_duty)
      
      if inputer_sender_lopper >= 5:
        asyncio.run( supabase_manager.send_ph_value_to_database(
            float(get_ph_value())
          ))

        asyncio.run(supabase_manager.send_temp_value_to_database(
          float(tempdata())
          ))

        print("inputer_sender_lopper:",inputer_sender_lopper)

        inputer_sender_lopper = 0

        print(inputer_sender_lopper)
      

      # print(gpio.input(14))

      
      # relay stuff
      if STATE_RELAY1:
        gpio.output(relay_pin1,1)
        gpio.output(relay_pin3,1)
      elif STATE_RELAY2:
        gpio.output(relay_pin2,1)
        gpio.output(relay_pin3,1)
      # oxygen motor
      elif not STATE_RELAY3:
        if (datetx.minute > 10 and datetx.minute < 25) or (datetime.minute > 40 and datetx.minute < 55):
          gpio.output(relay_pin4,1)
      elif STATE_RELAY3:
        gpio.output(relay_pin4,1)
      else:
        gpio.output(relay_pin1,0)
        gpio.output(relay_pin2,0)
        gpio.output(relay_pin3,0)
        gpio.output(relay_pin4,0)

      

            
      
      # if clock() - initial_timer >= 50:
      #   break

      
      inputer_sender_lopper += 1

      # delay some time
      sleep(1)



except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
   print("Keyboard interrupt")


# # other errors
# except:
#    print("some error") 


finally:
   print("clean up") 
   gpio.cleanup() # cleanup all GPIO 

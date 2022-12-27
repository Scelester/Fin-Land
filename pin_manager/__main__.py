'''
 # @ Author: Nabin Paudel|Scelester
 # @ Create Time: 2022-12-27 01:36:52
 # @ Modified time: 2022-12-27 10:35:00
 # @ Description:
 '''



import RPi.GPIO as gpio
from time import sleep
from time import perf_counter as clock

# importing files
from food_servo import start_servo
from Dphsense import get_ph_value
import supabase_manager
import asyncio
import datetime
from threading import Thread
import json



# getting Database




# setting up goio keys
gpio.setmode(gpio.BCM)

# servo motor setup
gpio.setup(14, gpio.OUT) # output signal fo GPIO
food_dispenser_servo = gpio.PWM(14,50)    # setting frequency
servo_initial_duty = 1
food_timer = 5
STATE_SERVO = False



#----------------------------- Date & time sets ------------------------------
datetx = datetime.datetime.now()
print(str(datetx.hour)+"."+str(datetx.minute))




# --------------------------- Clock setup ------------------------------------
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
STATE_RELAY2 = True
STATE_RELAY3 = False



# --------------------------------- Inputs ----------------------------------

# Temp sensor setup
temppin = 23
gpio.setup(temppin,gpio.IN)
def tempdata(pin=temppin):
  return gpio.input(pin)


inputer_sender_lopper = 0









# ----------------------------------------------------------------
#                                                                 |
#                                                                 | 
#  Main Function that runs on one thread                          |
#                                                                 |
#                                                                 |
# ----------------------------------------------------------------


def main():
  if STATE_SERVO:
         start_servo(food_dispenser_servo, servo_initial_duty,food_timer)
      
  if inputer_sender_lopper >= 20:
    asyncio.run( supabase_manager.send_ph_value_to_database(
        float(get_ph_value()[0])
      ))

    asyncio.run( supabase_manager.send_voltage_value_to_database(
        float(get_ph_value()[1])
        ))

    asyncio.run(supabase_manager.send_temp_value_to_database(
      float(tempdata())
      ))
    inputer_sender_lopper = 0
  

  
  

  # print(gpio.input(14))

  
  # relay stuff
  if STATE_RELAY1:
    gpio.output(relay_pin1,0)
    gpio.output(relay_pin2,1)
    gpio.output(relay_pin3,0)
    gpio.output(relay_pin4,1)

  elif STATE_RELAY2:
    gpio.output(relay_pin1,1)
    gpio.output(relay_pin2,0)
    gpio.output(relay_pin3,0)
    gpio.output(relay_pin4,1)

  # oxygen motor
  elif not STATE_RELAY3:
    if (datetx.minute > 10 and datetx.minute < 25) or (datetx.minute > 40 and datetx.minute < 55):
      gpio.output(relay_pin4,0)
      gpio.output(relay_pin1,1)
      gpio.output(relay_pin2,1)
      gpio.output(relay_pin3,1)
  elif STATE_RELAY3:
    gpio.output(relay_pin4,0)
    gpio.output(relay_pin1,1)
    gpio.output(relay_pin2,1)
    gpio.output(relay_pin3,1)
  else:
    gpio.output(relay_pin1,1)
    gpio.output(relay_pin2,1)
    gpio.output(relay_pin3,1)
    gpio.output(relay_pin4,1)

  

        
  
  # if clock() - initial_timer >= 50:
  #   break

  
  inputer_sender_lopper += 1

  # delay some time
  sleep(0.9 )




# ----------------------------------------------------------------
#                                                                 |
#                                                                 |
#  Looping function that fetches data from the                    |
# supabase DB with low delay.. that runs on another thread        |
#                                                                 |
#                                                                 |
# ----------------------------------------------------------------

def constant_RDC_fetcher():
  while True:
    
    Recived_data = asyncio.run(supabase_manager.get_remote_control_data())

    RDC_id = Recived_data[0]
    RDC_upDATE = Recived_data[1]
    RDC_oxygen = Recived_data[2]
    RDC_PH  = Recived_data[3]
    RDC_time = Recived_data[1]

    if RDC_id > StoredData.get("RDC_ID"):
      pass










# ----------------------------------------------------------------
#                                                                 |
#                                                                 | 
#  Executions Below                                               |
#                                                                 |
#                                                                 |
# ----------------------------------------------------------------

try:
    while True:
      Thread(target=main).start()
      Thread(target=constant_RDC_fetcher).start()

      



except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
   print("Keyboard interrupt")


# # other errors
# except:
#    print("some error") 


finally:
   print("clean up") 
   gpio.cleanup() # cleanup all GPIO 

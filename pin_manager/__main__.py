'''
 # @ Author: Nabin Paudel|Scelester
 # @ Create Time: 2022-12-27 01:36:52
 # @ Modified time: 2022-12-27 10:35:00
 # @ Description: Main Src
 '''



import RPi.GPIO as gpio
from time import sleep
from time import perf_counter as clock
import asyncio
import datetime
from threading import Thread
import json


# importing files
from food_servo import start_servo,stop_servo
from Dphsense import get_ph_value
import supabase_manager
from send_mail import send_mail


# getting Database
import db_manager
master_db = db_manager.DBMS()


# setting up goio keys
gpio.setmode(gpio.BCM)

# servo motor setup
gpio.setup(14, gpio.OUT) # output signal fo GPIO
food_dispenser_servo = gpio.PWM(14,50)    # setting frequency
servo_initial_duty = 1
STATE_SERVO = False



#----------------------------- Date & time sets ------------------------------
datetx = datetime.datetime.now()
print(str(datetx.hour)+"."+str(datetx.minute))




# --------------------------- Clock setup ------------------------------------
initial_timer = clock()
initial_food_timer = initial_timer



# --------------------------- Relay stuff ------------------------------------
relay_pin1 = 16   # acidic motor
relay_pin2 = 20   # basic motor
relay_pin3 = 21   # oxygen motor
relay_pin4 = 26   # dispenser motor
gpio.setup(relay_pin1,gpio.OUT)
gpio.setup(relay_pin2,gpio.OUT)
gpio.setup(relay_pin3,gpio.OUT)
gpio.setup(relay_pin4,gpio.OUT)
STATE_RELAY1 = False     # acidic moter state
STATE_RELAY2 = False     # basic moter state
STATE_RELAY3 = False     # oxygen motor state
relay_RDC_Timer = 0      # time value that will
overrideRDC_mode = False    


# --------------------------------- Inputs ----------------------------------

# Temp sensor setup
temppin = 23
gpio.setup(temppin,gpio.IN)
def tempdata(pin=temppin):
  return gpio.input(pin)


inputer_sender_lopper = 0



# relay re-factor
def relay_factor(AM=1,BM=1,OM=1,DM=1):
    gpio.output(relay_pin1,AM)
    gpio.output(relay_pin2,BM)
    gpio.output(relay_pin3,OM)
    gpio.output(relay_pin4,BM)






# ----------------------------------------------------------------
#                                                                 |
#                                                                 | 
#  Main Function that runs on one thread                          |
#                                                                 |
#                                                                 |
# ----------------------------------------------------------------


def main():
  ph_valueNvolt = get_ph_value()
  temp_value = float(tempdata())
  
  if STATE_SERVO:
         start_servo(food_dispenser_servo, servo_initial_duty)
         stop_servo(food_dispenser_servo, servo_initial_duty)
      
  if inputer_sender_lopper >= 20:
    asyncio.run( supabase_manager.send_ph_value_to_database(
        ph=ph_valueNvolt[0]
      ))

    asyncio.run( supabase_manager.send_ph_voltage_to_database(
        voltage=ph_valueNvolt[1]
        ))

    asyncio.run(supabase_manager.send_temp_value_to_database(
      temp=temp_value
      ))
    inputer_sender_lopper = 0

  # print(gpio.input(14))

  
  # relay stuff
  if STATE_RELAY1:
    relay_factor(AM=0,DM=0)

  elif STATE_RELAY2:
    relay_factor(BM=0,OM=1)

  # oxygen motor
  elif not STATE_RELAY3:   # if oxygen motor is not already running
    if (datetx.minute > 10 and datetx.minute < 25) or (datetx.minute > 40 and datetx.minute < 55):
      gpio.output(relay_pin3,0)

  elif STATE_RELAY3:
    relay_factor(OM=0,DM=0)

  else:
    relay_factor()

  if not overrideRDC_mode:
    if ph_valueNvolt[0] < 6:
      STATE_RELAY1 = True
    if ph_valueNvolt[0] > 9:
      STATE_RELAY2 = True
    if temp_value >= 30:
      send_mai("Temperature High", f"Your Fishtank Temperature is {temp_value}.")
    elif temp_value <= 19:
      send_mail("Temprature Low", f"Your Fishtank Temperature is {temp_value}.")

  if (initial_food_timer/60) > 10:
    STATE_SERVO = True
    initial_food_timer = clock()
  elif (initial_food_timer/60) > 1:
    STATE_SERVO = False
     

        
  
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

    # check if there was change in supabase rcd table
    prev_id = master_db.get_rdc("ID")
    if RDC_id > prev_id:
      relay_RDC_Timer = clock()
      overrideRDC_mode = True
      master_db.update_rdc("ID", RDC_id, previd=prev_id)
      
    if overrideRDC_mode:
      if int(clock() - relay_RDC_Timer) > RDC_time:
        overrideRDC_mode = False
        STATE_RELAY1 = False
        STATE_RELAY2 = False
        STATE_RELAY3 = False

      elif RDC_oxygen == 1:
        STATE_RELAY3 = True

      elif RDC_PH == 1:
        STATE_RELAY1 = True

      elif RDC_PH == 2:
        STATE_RELAY3 = True








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
   
   # closing database
   master_db.close()

   gpio.cleanup() # cleanup all GPIO 

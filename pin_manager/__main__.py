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
from gpiozero import Servo



# for adc imports 
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn  



# importing files
import supabase_manager
from send_mail import send_mail
from Dphsense import get_ph_value


def get_data_from_file():
  with open('pin_manager/datafile.txt', 'r') as file:
    context = file.readline()
    context = context.split(',')
    return context

def reset_data_from_file():
  with open('pin_manager/datafile.txt', 'w') as file:
    x = '10' + "," +  'somedate' + "," +  '0' + "," +  '0' + ","+ '0' + "," +  "0"
    file.write(x)

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

reset_data_from_file()

  # setting up goio keys

# servo motor setup
servo = Servo(14) # output signal fo GPIO

STATE_SERVO = False

#----------------------------- Date & time sets ------------------------------
datetx = datetime.datetime.now()



# --------------------------- Clock setup ------------------------------------
initial_timer = clock()
initial_food_timer = clock()




# --------------------------- Relay stuff ------------------------------------
relay_pin1 = 26   # acidic motor
relay_pin2 = 21   # basic motor
relay_pin3 = 20    # oxygen motor
relay_pin4 = 16    # dispenser motor
gpio.setup(relay_pin1,gpio.OUT)
gpio.setup(relay_pin2,gpio.OUT)
gpio.setup(relay_pin3,gpio.OUT)
gpio.setup(relay_pin4,gpio.OUT)
STATE_RELAY1 = False     # acidic moter state
STATE_RELAY2 = False     # basic moter state
STATE_RELAY3 = False     # oxygen motor state
relay_RDC_Timer = 0      # time value that will


# --------------------------------- Inputs ----------------------------------

# Temp sensor setup
temppin = 23
gpio.setup(temppin,gpio.IN)


# counter variables
inputer_sender_lopper = 0
relay_sender_looper = 0

# show time
print("TIME: "+str(datetx.hour)+"."+str(datetx.minute))

# before loop load remote variables
set_after_get_data_from_file()



def tempdata():
  return gpio.input(temppin)


# relay re-factor
def relay_factor(AM=1,BM=1,OM=1,DM=1):
  gpio.output(relay_pin1,AM)
  gpio.output(relay_pin2,BM)
  gpio.output(relay_pin3,OM)
  gpio.output(relay_pin4,BM)

def set_after_get_data_from_file():
  ggfilevar = get_data_from_file()
  RDC_id = ggfilevar[0]
  RDC_upDATE = ggfilevar[1]
  RDC_oxygen = int(ggfilevar[2])
  RDC_PH = int(ggfilevar[3])
  RDC_time = int(ggfilevar[4])
  overrideRDC_mode = ggfilevar[5]

""""""


  
# ----------------------------------------------------------------
#                                                                 |
#                                                                 | 
#  MAIN TO-BE-THREADed Function that runs on one thread           |
#                                                                 |
#                                                                 |
# ----------------------------------------------------------------    





# ----------------------------------------------------------------
#                                                                 |
#                                                                 | 
#  Executions Below                                               |
#                                                                 |
#                                                                 |
# ----------------------------------------------------------------
if __name__ == '__main__':
  try:
    while True:
      set_after_get_data_from_file()
      ph_valueNvolt = get_ph_value()
      temp_value = float(tempdata())

      if STATE_SERVO:
          servo.min()
          sleep(0.5)
          servo.mid()
          sleep(0.5)
          servo.max()
          STATE_SERVO = False
      else:
        if relay_sender_looper == 10:
          relay_sender_looper = 0
          servo.max()
          sleep(0.5)
          servo.mid()
          sleep(0.5)
          servo.min()
          sleep(1)

      
          
      if inputer_sender_lopper >= 20:
        asyncio.run( supabase_manager.send_ph_value_to_database(
            ph=ph_valueNvolt[0],voltage=ph_valueNvolt
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
        relay_factor(BM=0,DM=0)

      # oxygen motor
      elif not STATE_RELAY3:   # if oxygen motor is not already running
        if (datetx.minute > 10 and datetx.minute < 25) or (datetx.minute > 40 and datetx.minute < 55):
          relay_factor(OM=0)

      elif STATE_RELAY3:
        relay_factor(OM=0)

      else:
        relay_factor()

      if overrideRDC_mode == '0':
        if ph_valueNvolt[0] < 6:
          STATE_RELAY1 = True
        elif ph_valueNvolt[0] > 9:
          STATE_RELAY2 = True

        if temp_value >= 30:
          send_mai("Temperature High", f"Your Fishtank Temperature is {temp_value}.")
        elif temp_value <= 19:
          send_mail("Temprature Low", f"Your Fishtank Temperature is {temp_value}.")

      elif overrideRDC_mode == '1':
        relay_RDC_Timer = clock()
        if int(clock() - relay_RDC_Timer) >= RDC_time:
          reset_data_from_file()
          STATE_RELAY1 = False
          STATE_RELAY2 = False
          STATE_RELAY3 = False

        elif RDC_oxygen == 1:
          STATE_RELAY3 = True

        elif RDC_PH == 1:
          STATE_RELAY1 = True

        elif RDC_PH == 2:
          STATE_RELAY3 = True

      if initial_food_timer >= 60:
        STATE_SERVO = True
        initial_food_timer = 0
      elif initial_food_timer >= 10:
        STATE_SERVO = False
      

      # if clock() - initial_timer >= 50:
      #   

      
      inputer_sender_lopper += 1
      relay_sender_looper += 1

      # delay some time
      sleep(0.9)




  except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    print("Keyboard interrupt")
    
    

  # other errors
  except:
     print("some error") 
  finally:

    # cleaning up the data
    gpio.cleanup()
    print("clean up")

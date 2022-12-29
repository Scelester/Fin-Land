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



class main():
  def __init__(self):

    reset_data_from_file()

    # setting up goio keys
    gpio.setmode(gpio.BCM)

    # servo motor setup
    self.servo = Servo(14) # output signal fo GPIO

    self.STATE_SERVO = False

    #----------------------------- Date & time sets ------------------------------
    self.datetx = datetime.datetime.now()



    # --------------------------- Clock setup ------------------------------------
    self.initial_food_timer = clock()



    # --------------------------- Relay stuff ------------------------------------
    self.relay_pin1 = 26   # acidic motor
    self.relay_pin2 = 21   # basic motor
    self.relay_pin3 = 20    # oxygen motor
    self.relay_pin4 = 16    # dispenser motor
    gpio.setup(self.relay_pin1,gpio.OUT)
    gpio.setup(self.relay_pin2,gpio.OUT)
    gpio.setup(self.relay_pin3,gpio.OUT)
    gpio.setup(self.relay_pin4,gpio.OUT)
    self.STATE_RELAY1 = False     # acidic moter state
    self.STATE_RELAY2 = False     # basic moter state
    self.STATE_RELAY3 = False     # oxygen motor state
    self.relay_RDC_Timer = 0      # time value that will


    # --------------------------------- Inputs ----------------------------------

    # Temp sensor setup
    self.temppin = 23
    gpio.setup(self.temppin,gpio.IN)
    


    self.inputer_sender_lopper = 0

    print(str(self.datetx.hour)+"."+str(self.datetx.minute))
    # shared vairable
    
    self.ggfilevar = get_data_from_file()

    self.set_after_get_data_from_file()



  def tempdata(self):
    return gpio.input(self.temppin)


  # relay re-factor
  def relay_factor(self,AM=1,BM=1,OM=1,DM=1):
    gpio.output(self.relay_pin1,AM)
    gpio.output(self.relay_pin2,BM)
    gpio.output(self.relay_pin3,OM)
    gpio.output(self.relay_pin4,BM)

  def set_after_get_data_from_file(self):
    self.RDC_id = self.ggfilevar[0]
    self.RDC_upDATE = self.ggfilevar[1]
    self.RDC_oxygen = int(self.ggfilevar[2])
    self.RDC_PH = int(self.ggfilevar[3])
    self.RDC_time = int(self.ggfilevar[4])
    self.overrideRDC_mode = self.ggfilevar[5]

  """"""
  

      
  # ----------------------------------------------------------------
  #                                                                 |
  #                                                                 | 
  #  MAIN TO-BE-THREADed Function that runs on one thread           |
  #                                                                 |
  #                                                                 |
  # ----------------------------------------------------------------    
  def default(self):
    while True:
      self.relay_factor()
      self.set_after_get_data_from_file()
      ph_valueNvolt = get_ph_value()
      temp_value = float(self.tempdata())

      print(gpio.input(23))
      if self.STATE_SERVO:
          self.servo.min()
          sleep(0.5)
          self.servo.mid()
          sleep(0.5)
          self.servo.max()
          sleep(1)
          self.servo.mid()
          sleep(1)
          self.servo.max()
          self.STATE_SERVO = False
      else:
        self.servo.max()
        sleep(0.5)
        self.servo.mid()
        sleep(0.5)
        self.servo.min()
        sleep(1)

     
          
      if self.inputer_sender_lopper >= 20:
        asyncio.run( supabase_manager.send_ph_value_to_database(
            ph=ph_valueNvolt[0]
          ))

        asyncio.run( supabase_manager.send_ph_voltage_to_database(
            voltage=ph_valueNvolt[1]
            ))

        asyncio.run(supabase_manager.send_temp_value_to_database(
          temp=temp_value
          ))
        self.inputer_sender_lopper = 0

      # print(gpio.input(14))

      
      # relay stuff
      if self.STATE_RELAY1:
        self.relay_factor(AM=0,DM=0)

      elif self.STATE_RELAY2:
        self.relay_factor(BM=0,DM=0)

      # oxygen motor
      elif not self.STATE_RELAY3:   # if oxygen motor is not already running
        if (self.datetx.minute > 10 and self.datetx.minute < 25) or (self.datetx.minute > 40 and self.datetx.minute < 55):
          gpio.output(self.relay_pin3,0)

      elif self.STATE_RELAY3:
        self.relay_factor(OM=0,DM=0)

      else:
        self.relay_factor()

      if self.overrideRDC_mode == '0':
        if ph_valueNvolt[0] < 6:
          self.STATE_RELAY1 = True
        if ph_valueNvolt[0] > 9:
          self.STATE_RELAY2 = True
        if temp_value >= 30:
          send_mai("Temperature High", f"Your Fishtank Temperature is {temp_value}.")
        elif temp_value <= 19:
          send_mail("Temprature Low", f"Your Fishtank Temperature is {temp_value}.")
      else:
        self.relay_RDC_Timer = clock()
        if int(clock() - self.relay_RDC_Timer) > RDC_time:
          reset_data_from_file()
          self.STATE_RELAY1 = False
          self.STATE_RELAY2 = False
          self.STATE_RELAY3 = False

        elif self.RDC_oxygen == 1:
          self.STATE_RELAY3 = True

        elif self.RDC_PH == 1:
          self.STATE_RELAY1 = True

        elif RDC_PH == 2:
          self.STATE_RELAY3 = True

      if self.initial_food_timer >= 60:
        self.STATE_SERVO = True
        self.initial_food_timer = 0
      elif self.initial_food_timer >= 10:
        self.STATE_SERVO = False
     

      # if clock() - self.initial_timer >= 50:
      #   

      
      self.inputer_sender_lopper += 1

      # delay some time
      sleep(1)
  
  
  # ----------------------------------------------------------------
  #                                                                 |
  #                                                                 |
  #  Looping function that fetches data from the                    |
  # supabase DB with low delay.. that runs on another thread        |
  #                                                                 |
  #                                                                 |
  # ----------------------------------------------------------------|
        













# ----------------------------------------------------------------
#                                                                 |
#                                                                 | 
#  Executions Below                                               |
#                                                                 |
#                                                                 |
# ----------------------------------------------------------------
if __name__ == '__main__':
  try:
      FINLAND_BACKEND = main()
      FINLAND_BACKEND.default()

  except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    print("Keyboard interrupt")
    print("clean up") 
    gpio.cleanup()
    

  # # other errors
  # except:
  #    print("some error") 
  finally:
    print("clean up")
    gpio.cleanup() # cleanup all GPIO 



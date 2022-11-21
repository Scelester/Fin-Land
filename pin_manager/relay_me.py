from time import sleep
import RPi.GPIO as gpio



def relay_module(RPIN):
  gpio.output(RPIN,0)
  sleep(1)
  gpio.output(RPIN,1)
  sleep(6)

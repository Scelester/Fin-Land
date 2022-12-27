'''
 # @ Author: Nabin Paudel|Scelester
 # @ Create Time: 2022-12-13 23:11:20
 # @ Modified time: 2022-12-27 10:36:20 
 # @ Description: retrive PH sensor data using ADC 
 '''


import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
# ------------------------------





def get_ph_value():
    # create the spi bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D5)

    # create the mcp object
    mcp = MCP.MCP3008(spi, cs)

    # create an analog input channel on pin 0 
    chan = AnalogIn(mcp, MCP.P1)


    print('Raw ADC Value: ', chan.value)
    print('ADC Voltage: ' + str(chan.voltage) + 'V')
    
    phval = (float(chan.voltage) * 1024) / 5 / 60
    
    return phval

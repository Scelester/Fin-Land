'''
 # @ Author: Your name
 # @ Create Time: 2022-12-27 09:58:35
 # @ Modified by: Your name
 # @ Modified time: 2022-12-27 10:30:05
 # @ Description:
 '''

from threading import Thread
import asyncio
from .. import pin_manager
import time

def funny_controller():
    x = 1
    while True:
        print("nabin is ",x)
        time.sleep(1)



while True:
    Thread(target=funny_controller).start()
    Thread(target=(lambda:print("lmao"))).start()

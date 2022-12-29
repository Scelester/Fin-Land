'''
 # @ Author: Your name
 # @ Create Time: 2022-12-27 09:58:35
 # @ Modified by: Your name
 # @ Modified time: 2022-12-27 10:30:05
 # @ Description:
 '''

from threading import Thread
import asyncio
from time import sleep

# def funny_controller():
#     x = 1
#     while True:
#         print("nabin is ",x)
#         time.sleep(1)



# while True:
#     Thread(target=funny_controller).start()
#     Thread(target=(lambda:print("lmao"))).start()

def x():
    while True:
        print("x")
        sleep(2)

Thread(target=x).start()
while True:
    print("y")
    sleep(2)

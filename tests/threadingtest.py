from threading import Thread
from time import sleep
import asyncio



# man = "man"

# def x():
#     while True:
#         print("X")
#         print(man)
#         sleep(3)
        

# def z(payload):
#     print(payload)
#     sleep(1)


# def zwrapper(payload):
#     z(payload)

# def y():
#     while True:
#         print("y")
#         sleep(1)
#         Thread(target=zwrapper,args=["payload"]).start()


# Thread(target=x).start()
# Thread(target=y).start()

async def xmain():
    while True:
        print(";;gg")
        sleep(2)

async def this():
    print("nabin")

loop = asyncio.get_event_loop()

async def main():
    f1 = loop.create_task(xmain())
    f2 = loop.create_task(this())
    await asyncio.wait([f1,f2])

loop.run_until_complete(main())
loop.close()
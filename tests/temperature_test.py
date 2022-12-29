from RPi import GPIO
from time import sleep


GPIO.setmode(GPIO.BCM)

GPIO.setup(23,GPIO.IN)
try:
    while True:
        print(GPIO.input())
        sleep(5)

except KeyboardInterrupt:
    print("quit by user")
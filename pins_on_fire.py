import RPi.GPIO as gpio
from time import sleep

gpio.setwarnings(False)

gpio.setmode(gpio.BCM)
gpio.setup(14, gpio.OUT)

food_dispenser_servo = gpio.PWM(14,50)

duty = 5
x = 0

try:
    while True:
        print("11111111111111111111111111111")
        food_dispenser_servo.start(0)
        sleep(0.5)
        if x < 20:
            print("2222222222222222222222")
            food_dispenser_servo.ChangeDutyCycle(duty)
            duty += 1
            x += 1

        else:
            # food_dispenser_servo.changeDutyCycle(0)
            food_dispenser_servo.stop()
            gpio.cleanup()

            print("loop broke")
            break

except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
   print("Keyboard interrupt")

except:
   print("some error") 

finally:
   print("clean up") 
   gpio.cleanup() # cleanup all GPIO 
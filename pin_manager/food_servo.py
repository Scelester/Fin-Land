from time import sleep

def start_servo(servo,duty):
    servo.start(0)
    print(222222)
    servo.ChangeDutyCycle(20)
    sleep(5)
    duty = 1
    servo.ChangeDutyCycle(duty)
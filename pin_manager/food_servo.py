from time import sleep

def start_servo(servo,duty):
    servo.start(0)

    servo.ChangeDutyCycle(duty)

    duty = 20
    
    servo.ChangeDutyCycle(duty)
    
    sleep(5)
    duty = 1
    servo.ChangeDutyCycle(duty)
from time import sleep

def start_servo(servo,duty):
    servo.start(0)
    print("================ servo running =========================")

    # servo.ChangeDutyCycle(duty)              -> test remaning
    
    
    duty = 17 # rotating to about 170 degrees
    servo.ChangeDutyCycle(duty)
    
    # print(">> Changed duty cycle to initial value :20")

    # sleep(timer)
    # duty = 1
    # servo.ChangeDutyCycle(duty)
    # print(">> Resetting duty cycle to initial value :1")

    
def stop_servo(servo,duty):
    print("stop Servo")
    servo.ChangeDutyCycle(duty)

from time import sleep

def start_servo(servo,duty):
    servo.start(0)
    print("================ servo running =========================")
    
    servo.ChangeDutyCycle(duty)
    
    
    duty = 17 # rotating to about 170 degrees
    servo.ChangeDutyCycle(duty)
    
    print(">> Changed duty cycle to initial value :20")

    sleep(10)
    duty = 1
    servo.ChangeDutyCycle(duty)
    print(">> Resetting duty cycle to initial value :1")

    servo.stop()

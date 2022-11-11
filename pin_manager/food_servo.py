from time import sleep

def start_servo(servo,duty):
    servo.start(0)
    print("11111")
    while duty < 9:
        print(222222)
        servo.ChangeDutyCycle(duty)
        duty += 3
        sleep(1)
        print(33333)

    duty = 1
    sleep(3)
    servo.ChangeDutyCycle(duty)
    print("food 1 cycle")
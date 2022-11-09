


def start_servo(servo,duty):
    servo.start(0)
            
    while duty < 9:
        servo.ChangeDutyCycle(duty)
        duty += 3
        sleep(1)

    duty = 1
    sleep(3)
    servo.ChangeDutyCycle(duty)
    print("food 1 cycle")
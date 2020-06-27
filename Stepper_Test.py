import PiMotor
import time
import RPi.GPIO as GPIO

m1 = PiMotor.Stepper("STEPPER1")

# Rotate Stepper 1 Contiously in forward/backward direction
try:
    while True:
        m1.forward(0.1,100)  # Delay and rotations
        time.sleep(2)
        m1.backward(0.1,100)
        time.sleep(2)
finally:
    GPIO.cleanup()

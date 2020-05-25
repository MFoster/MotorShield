import PiMotor
import time
import RPi.GPIO as GPIO
import AdvancedStepper

motor = AdvancedStepper("STEPPER1")

# Rotate Stepper 1 Contiously in forward/backward direction
try:
    while True:
        motor.forward(200)  # Delay and rotations
        time.sleep(2)
        motor.backward(200)
        time.sleep(2)
        motor.setMode("double")
        motor.forward(200)
        time.sleep(2)
        motor.backward(200)
        motor.setMode("half")
        motor.forward(200)
        time.sleep(2)
        motor.backward(200)
        time.sleep(2)

except KeyboardInterrupt:
    GPIO.cleanup()

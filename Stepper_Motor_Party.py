from PiMotor import PolarStepper
import time
from RPi import GPIO


motor = PolarStepper("STEPPER1")
delay = 0.01
steps = 200
# Rotate Stepper 1 Contiously in forward/backward direction
try:
    #while True:
        print("Back and forth with the half step")
        motor.setMode("half")
        motor.forward(delay, steps * 2)
        motor.backward(delay, steps * 2)  # Delay and rotations
        print("Two steps with a full steps")
        motor.setMode("full")
        motor.backward(delay, steps)
        motor.forward(delay, steps)
        print("One last time, feel the wave!")
        motor.setMode("wave")
        motor.forward(delay, steps)
        motor.backward(delay, steps)

finally:
    GPIO.cleanup()
                                                
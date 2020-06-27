"""
Exercises the motor through the various modes, half, double and single.
If using a unipolar you may see erratic behavior from the motorduring single 
without the common wires connected.
"""
from PiMotor import Stepper
import time
from RPi import GPIO


motor = Stepper("STEPPER1")
delay = 0.01
steps = 200
try:
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

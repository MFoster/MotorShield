"""
Starts fast and slows down as it comes to a stop.
"""
from PiMotor import Stepper
import time
from RPi import GPIO
from easy import EasyStepper

motor = Stepper("STEPPER1")
motor.setMode("half")
ez = EasyStepper(start=0.05, end=0.5)
steps = 400

try:
    print("Back and forth with the half step")
    motor.forward(ez.quad(steps), steps)
    motor.backward(ez.quad(steps), steps)
finally:
    GPIO.cleanup()
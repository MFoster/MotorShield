"""
Demonstrates ability to ease into and out of speed changes in either direction on the motor.
"""
from PiMotor import Stepper
from RPi import GPIO
from easy import EasyStepperSequence
from easing_functions import *

motor = Stepper("STEPPER1")
motor.setMode("half")
steps = 1600
initial_speed = 0.05
final_speed = 0.05
top_speed = 0.01
# Rotate Stepper 1 Contiously in forward/backward direction
try:
    print("Ease up into full speed and back down with quad ease in and out")
    sequence = EasyStepperSequence(initial_speed, steps)
    sequence.append(QuadEaseIn, top_speed, 0.5)
    sequence.append(QuadEaseOut, final_speed, 0.5)
    sequence.execute(motor.forward)
    sequence.execute(motor.backward)
finally:
    GPIO.cleanup()
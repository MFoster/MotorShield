#!/usr/bin/python

# Library for PiMotor Shield V2
# Developed by: SB Components
# Project: RPi Motor Shield

import RPi.GPIO as GPIO                        #Import GPIO library
import time, logging
from time import sleep
GPIO.setmode(GPIO.BOARD)                       #Set GPIO pin numbering

GPIO.setwarnings(False)

class Motor:
    """ Class to handle interaction with the motor pins
    Supports redefinition of "forward" and "backward" depending on how motors are connected
    Use the supplied Motorshieldtest module to test the correct configuration for your project.

    Arguments:
    motor = string motor pin label (i.e. "MOTOR1","MOTOR2","MOTOR3","MOTOR4") identifying the pins to which
            the motor is connected.
    config = int defining which pins control "forward" and "backward" movement.
    """
    motorpins = {"MOTOR4":{"config":{1:{"e":32,"f":24,"r":26},2:{"e":32,"f":26,"r":24}},"arrow":1},
                 "MOTOR3":{"config":{1:{"e":19,"f":21,"r":23},2:{"e":19,"f":23,"r":21}}, "arrow":2},
                 "MOTOR2":{"config":{1:{"e":22,"f":16,"r":18},2:{"e":22,"f":18,"r":16}}, "arrow":3},
                 "MOTOR1":{"config":{1:{"e":11,"f":15,"r":13},2:{"e":11,"f":13,"r":15}},"arrow":4}}

    def __init__(self, motor, config):
        self.testMode = False
        self.arrow = Arrow(self.motorpins[motor]["arrow"])
        self.pins = self.motorpins[motor]["config"][config]
        GPIO.setup(self.pins['e'],GPIO.OUT)
        GPIO.setup(self.pins['f'],GPIO.OUT)
        GPIO.setup(self.pins['r'],GPIO.OUT)
        self.PWM = GPIO.PWM(self.pins['e'], 50)  # 50Hz frequency
        self.PWM.start(0)
        GPIO.output(self.pins['e'],GPIO.HIGH)
        GPIO.output(self.pins['f'],GPIO.LOW)
        GPIO.output(self.pins['r'],GPIO.LOW)

    def test(self, state):
        """ Puts the motor into test mode
        When in test mode the Arrow associated with the motor receives power on "forward"
        rather than the motor. Useful when testing your code.

        Arguments:
        state = boolean
        """
        self.testMode = state

    def forward(self, speed):
        """ Starts the motor turning in its configured "forward" direction.

        Arguments:
        speed = Duty Cycle Percentage from 0 to 100.
        0 - stop and 100 - maximum speed
        """
        print("Forward")
        if self.testMode:
            self.arrow.on()
        else:
            self.PWM.ChangeDutyCycle(speed)
            GPIO.output(self.pins['f'],GPIO.HIGH)
            GPIO.output(self.pins['r'],GPIO.LOW)

    def reverse(self,speed):
        """ Starts the motor turning in its configured "reverse" direction.

        Arguments:
        speed = Duty Cycle Percentage from 0 to 100.
        0 - stop and 100 - maximum speed
     """
        print("Reverse")
        if self.testMode:
            self.arrow.off()
        else:
            self.PWM.ChangeDutyCycle(speed)
            GPIO.output(self.pins['f'],GPIO.LOW)
            GPIO.output(self.pins['r'],GPIO.HIGH)

    def stop(self):
        """ Stops power to the motor,
     """
        print("Stop")
        self.arrow.off()
        self.PWM.ChangeDutyCycle(0)
        GPIO.output(self.pins['f'],GPIO.LOW)
        GPIO.output(self.pins['r'],GPIO.LOW)

    def speed(self):
        """ Control Speed of Motor,
     """

class LinkedMotors:
    """ Links 2 or more motors together as a set.

        This allows a single command to be used to control a linked set of motors
        e.g. For a 4x wheel vehicle this allows a single command to make all 4 wheels go forward.
        Starts the motor turning in its configured "forward" direction.

        Arguments:
        *motors = a list of Motor objects
     """
    def __init__(self, *motors):
        self.motor = []
        for i in motors:
            print(i.pins)
            self.motor.append(i)

    def forward(self,speed):
        """ Starts the motor turning in its configured "forward" direction.

        Arguments:
        speed = Duty Cycle Percentage from 0 to 100.
        0 - stop and 100 - maximum speed
     """
        for i in range(len(self.motor)):
            self.motor[i].forward(speed)

    def reverse(self,speed):
        """ Starts the motor turning in its configured "reverse" direction.

        Arguments:
        speed = Duty Cycle Percentage from 0 to 100.
        0 - stop and 100 - maximum speed
     """
        for i in range(len(self.motor)):
            self.motor[i].reverse(speed)

    def stop(self):
        """ Stops power to the motor,
     """
        for i in range(len(self.motor)):
            self.motor[i].stop()

class Stepper:
    """ 
    Defines stepper motor class to control bipolar and unipolar
    stepper motors.

    Arguments:
    motor = stepper motor pin configuration.
            values can be STEPPER1 or STEPPER2.  This corresponds to the
            ports on the motor shield itself.
    """

    """
    Pin configuration for Rapsberry Pi GPIO to Motor Shield stepper motor interface
    """
    stepperpins = {"STEPPER1":{"en1":11, "en2":22, "c1":13,"c2":15, "c3":18, "c4":16},
                   "STEPPER2":{"en1":19, "en2":32, "c1":21,"c2":23, "c3":24, "c4":26}}

    """
    Least torque, most efficient.
    Commonly referred to as wave drive or single step.
    """
    single_mode = [[1, 0, 0, 0],
                   [0, 1, 0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]]
    """
    Most torque, least efficient.
    Commonly referred to as full step
    """
    double_mode = [[1, 0, 1, 0],
                   [0, 1, 1, 0],
                   [0, 1, 0, 1],
                   [1, 0, 0, 1]]
    """
    Good blend of strength and efficiency. Doubles step resolution, therefore increasing accuracy
    and can reduce slippage on high load operations.
    If you had a 1.8 deg stepper at 200 steps per revolution and you choose half
    step mode, then you have 0.9 deg stepper at 400 steps per revolution.
    """
    half_mode = [[1, 0, 0, 0],
                 [1, 0, 1, 0],
                 [0, 0, 1, 0],
                 [0, 1, 1, 0],
                 [0, 1, 0, 0],
                 [0, 1, 0, 1],
                 [0, 0, 0, 1],
                 [1, 0, 0, 1]]

    """
    Default the mode to single
    """
    mode = single_mode

    def __init__(self, motor):
        self.config = self.stepperpins[motor]
        GPIO.setup(self.config["en1"],GPIO.OUT)
        GPIO.setup(self.config["en2"],GPIO.OUT)
        GPIO.setup(self.config["c1"],GPIO.OUT)
        GPIO.setup(self.config["c2"],GPIO.OUT)
        GPIO.setup(self.config["c3"],GPIO.OUT)
        GPIO.setup(self.config["c4"],GPIO.OUT)

        GPIO.output(self.config["en1"],GPIO.HIGH)
        GPIO.output(self.config["en2"],GPIO.HIGH)
        GPIO.output(self.config["c1"],GPIO.LOW)
        GPIO.output(self.config["c2"],GPIO.LOW)
        GPIO.output(self.config["c3"],GPIO.LOW)
        GPIO.output(self.config["c4"],GPIO.LOW)

    def setMode(self, mode):
        """
        mode: str -- values can be half, double or full every other value defaults to single.
        Sets the sequence in which the coils will fire.
        """
        if(mode == "double" or mode == "full"):
            self.mode = self.double_mode
        elif(mode == "half"):
            self.mode = self.half_mode
        else:
            self.mode = self.single_mode
    

    def setStep(self, w1, w2, w3, w4):
        """ 
        Energize the stepper motor's coils in sequence to create motion.
        Avoid energizing both sides of the same coil.

        Arguments:
        w1,w2,w3,w4 = Wire of Stepper Motor
        """
        if(w1 > 0 and w2 > 0 or w3 > 0 and w4 > 0):
            logging.warn("cross coil interference")

        GPIO.output(self.config["c1"], w1)
        GPIO.output(self.config["c2"], w2)
        GPIO.output(self.config["c3"], w3)
        GPIO.output(self.config["c4"], w4)

    def forward(self, delay, steps):
        """ 
        Rotate Stepper motor in forward direction

        Arguments:
        delay: 
            float - value for seconds between steps, typically value is less than 1.
            lambda - send a lambda that will be executed each iteration and sent the current step and total step count, 
            the lambda must then return a float value that will be used as the delay for that step.  
            This allows for acceleration and deceleration during a sequence of steps.

        steps: int - Number of Steps
        """
        seq_len = len(self.mode)
        for index in range(steps):
            if(index > 0 and callable(delay)): time.sleep(delay(index, steps))
            elif(index > 0): time.sleep(delay)
            self.setStep(*self.mode[index % seq_len])


    def backward(self, delay, steps):
        """ 
        Rotate Stepper motor in opposite direction

        Arguments:
        delay: 
            float - value for seconds between steps, typically value is less than 1.
            lambda - send a lambda that will be executed each iteration and sent the current step and total step count, 
            the lambda must then return a float value that will be used as the delay for that step.  
            This allows for acceleration and deceleration during a sequence of steps.

        steps: int - Number of Steps
        """
        seq_len = len(self.mode)
        for index in range(steps):
            if(index > 0 and callable(delay)): time.sleep(delay(index, steps))
            elif(index > 0): time.sleep(delay)
            self.setStep(*reversed(self.mode[index % seq_len]))
    
    
    def stop(self):
        """ 
        Stops power to the motor,
        """
        self.setStep(0, 0, 0, 0)

    def cleanup(self):
        """
        Convienence function so other packages don't have to import GPIO just 
        to execute cleanup
        """
        GPIO.cleanup()

class Sensor:
    """ Defines a sensor connected to the sensor pins on the MotorShield

        Arguments:
        sensortype = string identifying which sensor is being configured.
            i.e. "IR1", "IR2", "ULTRASONIC"
        boundary = an integer specifying the minimum distance at which the sensor
            will return a Triggered response of True.
    """
    Triggered = False
    def iRCheck(self):
        input_state = GPIO.input(self.config["echo"])
        if input_state == True:
            print("Sensor 2: Object Detected")
            self.Triggered = True
        else:
            self.Triggered = False

    def sonicCheck(self):
        print("SonicCheck has been triggered")
        time.sleep(0.333)
        GPIO.output(self.config["trigger"], True)
        time.sleep(0.00001)
        GPIO.output(self.config["trigger"], False)
        start = time.time()
        while GPIO.input(self.config["echo"])==0:
            start = time.time()
        while GPIO.input(self.config["echo"])==1:
            stop = time.time()
        elapsed = stop-start
        measure = (elapsed * 34300)/2
        self.lastRead = measure
        if self.boundary > measure:
            print("Boundary breached")
            print(self.boundary)
            print(measure)
            self.Triggered = True
        else:
            self.Triggered = False

    sensorpins = {"IR1":{"echo":7, "check":iRCheck}, "IR2":{"echo":12, "check":iRCheck},
                  "ULTRASONIC":{"trigger":29, "echo": 31, "check":sonicCheck}}

    def trigger(self):
        """ Executes the relevant routine that activates and takes a reading from the specified sensor.

        If the specified "boundary" has been breached the Sensor's Triggered attribute gets set to True.
    """
        self.config["check"](self)
        print("Trigger Called")

    def __init__(self, sensortype, boundary):
        self.config = self.sensorpins[sensortype]
        self.boundary = boundary
        self.lastRead = 0
        if "trigger" in self.config:
            print("trigger")
            GPIO.setup(self.config["trigger"],GPIO.OUT)
        GPIO.setup(self.config["echo"],GPIO.IN)

class Arrow():
    """ Defines an object for controlling one of the LED arrows on the Motorshield.

        Arguments:
        which = integer label for each arrow. The arrow number if arbitrary starting with:
            1 = Arrow closest to the Motorshield's power pins and running clockwise round the board
            ...
            4 = Arrow closest to the motor pins.
    """
    arrowpins={1:33,2:35,3:37,4:36}

    def __init__(self, which):
        self.pin = self.arrowpins[which]
        GPIO.setup(self.pin,GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

    def on(self):
        GPIO.output(self.pin,GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin,GPIO.LOW)
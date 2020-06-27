from easing_functions import *

class EasyStepper:
    """
    Eases implementation of using acceleration and deceleration with the stepper motor
    params:
        start: float -- initial delay.
        end: float -- delay at the end of step sequence.
    example:
        ez = EasyStepper(0.1, 0.01) # This will start it at relatively slow speed and then power up to a 10x faster speed.
        motor = Stepper("STEPPER1")
        motor.forward(ez.quad(200), 200) # Powers up to full speed using a quadratic function.
        motor.forward(ez.reverse().quad(200), 200) # Continues its forward direction but powers back down to its original speed before holding its final position
    """
    def __init__(self, start=0.05, end=0.1):
        self.start = start
        self.end = end

    def linear(self, steps):
        ez = LinearInOut(start=self.start, end=self.end, duration=steps)
        return lambda index, _: ez.ease(index)

    def quad(self, steps):
        ez = QuadEaseInOut(start=self.start, end=self.end, duration=steps)
        return lambda index, _: ez.ease(index)

    def circular(self, steps):
        ez = CircularEaseInOut(start=self.start, end=self.end, duration=steps)
        return lambda index, _: ez.ease(index)

    def expo(self, steps):
        ez = ExponentialEaseInOut(start=self.start, end=self.end, duration=steps)
        return lambda index, _: ez.ease(index)

    def elastic(self, steps):
        ez = ElasticEaseInOut(start=self.start, end=self.end, duration=steps)
        return lambda index, _: ez.ease(index)

    def back(self, steps):
        ez = BackEaseInOut(start=self.start, end=self.end, duration=steps)
        return lambda index, _: ez.ease(index)

    def bounce(self, steps):
        ez = BounceEaseInOut(start=self.start, end=self.end, duration=steps)
        return lambda index, _: ez.ease(index)

    def reverse(self):
        return EasyStepper(start=self.end, end=self.start)

class EasyStepperSequence:
    """
    Utility for executing complex acceleration and deceleration sequences.
    params:
        start -- float, initial delay that the sequence will begin with.
        steps -- int, total number of steps that will be taken during the sequence.
    example:
        sequence = EasyStepperSequence(initial_speed, steps)
        sequence.append(QuadEaseIn, top_speed, 0.5) # 0.5 for two items in the sequence means steps are shared equally
        sequence.append(QuadEaseOut, final_speed, 0.5)
        sequence.execute(motor.forward)
    """
    def __init__(self, start, steps):
        self.steps = steps
        self.start = start
        self.chain = []
    
    def append(self, func, speed, weight):
        """
        Add another link in the chain.
        params:
            func -- easing_function function, used to calculate delay during execution.  i.e. QuadEaseIn
            speed -- desired delay achieved at the end of the execution of this sequence.
            weight -- used to calculate how many steps this segment of the sequence will get to execute.
        """
        y = int(self.steps * weight)
        x = func(start=self.start, end=speed, duration=y)
        self.start = x.ease(y)
        self.chain.append((lambda idx, _: x.ease(idx), y))

    def execute(self, func):
        """
        Once the sequence is defined you can execute it against an existing PiMotor.Stepper instance.
        Pass the instance's forward or backward function as the func param.
        example:
            sequence.execute(motor.forward)
        params:
            func -- motor's forward or backward function.
        """
        for pair in self.chain:
            func(*pair)


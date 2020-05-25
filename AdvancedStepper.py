from PiMotor import Stepper

class AdvancedStepper(Stepper):
    single_step = [[1, 0, 0, 0],
                   [0, 1, 0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]]]
    
    double_step = [[1, 0, 1, 0],
                   [0, 1, 1, 0],
                   [0, 1, 0, 1],
                   [1, 0, 0, 1]]

    half_step = [[1, 0, 0, 0],
                 [1, 0, 1, 0],
                 [0, 0, 1, 0],
                 [0, 1, 1, 0],
                 [0, 1, 0, 0],
                 [0, 1, 0, 1],
                 [0, 0, 0, 1],
                 [1, 0, 0, 1]]
    
    mode = single_step

    delay = 0.1

    def setMode(self, mode):
        if(mode == "double"):
            self.mode = self.double_step
        elif(mode == "half"):
            self.mode = self.half_step
        else
            self.mode = self.single_step

    def forward(self, delay=self.delay, steps):
        for _ in range(steps):
            for seq in self.mode:
                self.setStep(*seq)
                timer.sleep(delay)

    def backward(self, delay=self.delay, steps):
        for _ in range(steps):
            for seq in self.mode:
                self.setStep(*reversed(seq))
                timer.sleep(delay)
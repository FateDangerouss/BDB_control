import PCA9685
import time

class Conveyor_belt:
    def __init__(self):
        self.setup()
    
    def setup(self):
        self.pwm = PCA9685.Steering_Gear(0x40, debug=False)
        self.pwm.setPWMFreq(50)
    
    def run(self, t):
        self.t = t
        self.pwm.setServoPulse(12, 2500)
        time.sleep(self.t)
        self.pwm.setServoPulse(12, 300)

import PCA9685
import time

class RoboticArm:
    def __init__(self, pin):
        self.pin = pin
        self.setup()
    
    def setup(self):
        self.pwm = PCA9685.Steering_Gear(0x40, debug=False)
        self.pwm.setPWMFreq(50)
    
    def run(self):
        self.pwm.setServoPulse(self.pin, 900)
        time.sleep(1.3)
        self.pwm.setServoPulse(self.pin, 2200)
        time.sleep(0.75)
        self.pwm.setServoPulse(self.pin, 300)
        
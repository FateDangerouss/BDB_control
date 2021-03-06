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
        self.pwm.setServoPulse(0,2200)
        time.sleep(0.9)
        self.pwm.setServoPulse(0,900)
        time.sleep(0.75)
        self.pwm.setServoPulse(0,300)
        
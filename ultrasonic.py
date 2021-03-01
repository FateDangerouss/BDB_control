import RPi.GPIO as GPIO
import time

class Ultrasonic:
    def __init__(self, TRIG, ECHO):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self.TRIG = TRIG
        self.ECHO = ECHO
        self.setup()
    
    def setup(self):
        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)
        
    def distance(self):
        GPIO.output(self.TRIG, GPIO.LOW)
        time.sleep(0.000002)

        GPIO.output(self.TRIG, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self.TRIG, GPIO.LOW)

        while GPIO.input(self.ECHO) == 0:
            pass
        time1 = time.time()

        while GPIO.input(self.ECHO) == 1:
            pass
        time2 = time.time()

        during = time2 - time1
        
        return during * 340 / 2 * 100
        
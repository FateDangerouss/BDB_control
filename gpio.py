import RPi.GPIO as GPIO

class myGPIO:
    def __init__(self, list):
        GPIO.setmode(GPIO.BCM)
        self.__disable_warning()
        self.setup(list)
    
    def __disable_warning(self):
        GPIO.setwarnings(False)
    
    def __enable_warning(self):
        GPIO.setwarnings(True)
    
    def setup(self, list):
        GPIO.setmode(GPIO.BCM)
        i = 0
        while i < len(list):
            if list[i+1] == "IN":
                GPIO.setup(list[i], GPIO.IN)
            if list[i+1] == "OUT":
                GPIO.setup(list[i], GPIO.OUT)
            i = i + 2
    
    def input(self, pin):
        GPIO.setmode(GPIO.BCM)
        return GPIO.input(pin)
    
    def output(self, pin, type):
        GPIO.setmode(GPIO.BCM)
        if type == "LOW":
            GPIO.output(pin, 0)
        if type == "HIGH":
            GPIO.output(pin, 1)
            
class PWM:
    def __init__(self, pin, frequency):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        self.run = GPIO.PWM(pin, frequency)
        
    def start(self, dc):
        self.run.start(dc)
            
    def changefreq(self, freq):
        self.run.ChangeFrequency(freq)
        
    def changedc(dc):
        self.run.ChangeDutyCycle(dc)
        
    def stop(self):
        self.run.stop()
    def destroy(self):
        self.stop()
        GPIO.cleanup()
        
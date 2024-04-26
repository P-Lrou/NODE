import RPi.GPIO as GPIO

class Led:
    def __init__(self, pin_number) -> None:
        self.pin_number = pin_number
        GPIO.setup(self.pin_number, GPIO.OUT)
        GPIO.output(self.pin_number, GPIO.LOW)
        self.state = GPIO.LOW
    
    def on(self):
        GPIO.output(self.pin_number, GPIO.HIGH)
        self.state = GPIO.HIGH
    
    def off(self):
        GPIO.output(self.pin_number, GPIO.LOW)
        self.state = GPIO.LOW

    def toggle(self):
        GPIO.output(self.pin_number, not self.state)
        self.state = not self.state

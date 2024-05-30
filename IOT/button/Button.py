import RPi.GPIO as GPIO
from tools.DLog import DLog

class Button:
    def __init__(self, pin: int, delegate=None):
        self.pin: int = pin
        self.has_joined: bool = False
        self.button_pressed: bool = False
        self.delegate = delegate
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    def process(self):
        input_state = GPIO.input(self.pin) == GPIO.HIGH
        if input_state and not self.button_pressed:
            self.has_joined = not self.has_joined
            if self.delegate:
                self.delegate.on_clicked(self)
        self.button_pressed = input_state


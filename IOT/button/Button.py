import RPi.GPIO as GPIO
from tools.DLog import DLog
from button.ButtonDelegate import ButtonDelegate

class Button:
    def __init__(self, pin: int, delegate: ButtonDelegate = None):
        self.button_pressed: bool = False
        self.delegate = delegate
        self.pin: int = pin
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    def process(self):
        input_state = GPIO.input(self.pin) == GPIO.LOW
        if input_state and not self.button_pressed:
            if self.delegate:
                self.delegate.on_clicked(button=self)
        self.button_pressed = input_state


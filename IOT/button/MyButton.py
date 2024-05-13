import RPi.GPIO as GPIO
import json

class MyButton:
    def __init__(self, pin:int, activity_type: str, delegate=None):
        self.pin:int = pin
        self.activity_type: str = activity_type
        self.has_joined:bool = False
        self.button_pressed:bool = False
        self.delegate = delegate
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    def process(self):
        input_state = GPIO.input(self.pin)
        if input_state and not self.button_pressed:
            if self.delegate:
                self.delegate.on_clicked(self)
        self.button_pressed = input_state

    def get_data(self):
        return {
            "type": "activity",
            "activity_type": self.activity_type,
            "state": "joined" if self.has_joined else "retired"
        }


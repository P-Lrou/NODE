import RPi.GPIO as GPIO
import json

class MyButton:
    def __init__(self, pin, ws_client):
        self.pin = pin
        self.ws_client = ws_client
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.button_pressed = False
        self.message_sent = False
    
    def send_message(self, data):
        self.ws_client.send(json.dumps(data))
    
    def process(self):
        while True:
            input_state = GPIO.input(self.pin)
            if not input_state and not self.button_pressed:
                self.button_pressed = True
                self.message_sent = False
            elif input_state and self.button_pressed and not self.message_sent:
                data = {
                            "type": "activity",
                            "activity_type": "belotte",
                            "state": "joined"
                        }
                self.ws_client.send_message(json.dumps(data))
                self.message_sent = True 
                self.button_pressed = False

    def close(self):
        GPIO.cleanup()


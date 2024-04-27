from GlobalVariables import *
from MyDelegates import *
import RPi.GPIO as GPIO

class IOTManager:
    def __del__(self):
        GPIO.cleanup()

    def __init__(self) -> None:
        #* Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        #* Websocket client
        from wsclient.WSClient import WSClient
        ws_client_callback = WSClientCallback()
        self.ws_client = WSClient.connectToVPS(ws_client_callback)

        #* Rfid reader
        from rfid.Rfid import Rfid
        rfid_callback = RfidCallback(self.ws_client)
        self.rfid = Rfid(rfid_callback)

        #* Led controller
        from led.LedController import LEDController
        self.led_matchmaking = LEDController(pin_numbers=LedPins.instance().matchmaking_number)
        self.led_activities = LEDController(pin_by_name=LedPins.instance().activities_led_number)
        self.led_controllers = [
            self.led_matchmaking,
            self.led_activities
        ]
    
    def start(self):
        self.ws_client.start()
        try:
            while True:
                self.rfid.process()
        except KeyboardInterrupt:
            print("End of the program")
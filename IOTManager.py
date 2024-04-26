from GlobalVariables import *
from MyDelegates import *

class IOTManager:
    def __del__(self):
        for led_controller in self.led_controllers:
            del led_controller

    def __init__(self) -> None:
        #* Websocket client
        from wsclient.WSClient import WSClient
        ws_client_callback = WSClientCallback()
        self.ws_client = WSClient.connectToVPS(ws_client_callback)

        #* Rfid reader
        from rfid.Rfid import Rfid
        rfid_callback = RfidCallback()
        self.rfid = Rfid(rfid_callback)

        #* Led controller
        from led.LedController import LEDController
        self.led_matchmaking = LEDController(pin_numbers=LedPins.instance.matchmaking_number)
        self.led_activities = LEDController(pin_by_name=LedPins.instance.activities_led_number)
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
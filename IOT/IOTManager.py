from GlobalVariables import *
from MyDelegates import *
from tools.DLog import DLog
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

        from button.MyButton import MyButton
        button_callback = ButtonCallback(self.ws_client)
        self.button = MyButton(18, "belotte", button_callback)

    
    def start(self):
        self.ws_client.start()
        try:
            while True:
                if self.ws_client.connected:
                    self.rfid.process()
                    self.button.process()
        except KeyboardInterrupt:
            DLog.Log("End of the program")

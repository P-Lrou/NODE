from GlobalVariables import *
from MyDelegates import *
from tools.DLog import DLog
from tools.LedDisplayer import LedDisplayer
import RPi.GPIO as GPIO
import sys
import time

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
        from rfid.RfidController import RfidController
        rfid_callback = RfidCallback(self.ws_client)
        self.rfid_controller = RfidController(rfid_callback)

        from button.MyButton import MyButton
        button_callback = ButtonCallback(self.ws_client)
        self.button = MyButton(18, "belotte", button_callback)

    def run_checks(self):
        LedDisplayer.setup()
        LedDisplayer.new_test_sequence()
        if self.rfid_controller.process_checker():
            LedDisplayer.test_passed()
        else:
            LedDisplayer.test_failed()
            LedDisplayer.cleanup()
            sys.exit()

        
        LedDisplayer.new_test_sequence()
        time.sleep(2)
        if self.ws_client.connected:
            LedDisplayer.test_passed()
        else:
            LedDisplayer.test_failed()
            LedDisplayer.cleanup()
            sys.exit()
            

    def start(self):
        try:
            self.ws_client.start()
            self.run_checks()
            while True:
                if self.ws_client.connected:
                    self.rfid_controller.process()
                    self.button.process()
        except KeyboardInterrupt:
            DLog.Log("End of the program")

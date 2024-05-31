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
        from wsclient.WebSocketDataSender import WebSocketDataSender
        ws_client_callback = WSClientCallback()
        self.ws_client = WSClient.connectToVPS(ws_client_callback)
        ws_data_sender = WebSocketDataSender(self.ws_client)

        #* Rfid reader
        from rfid.RfidController import RfidController
        rfid_callback = RfidCallback(ws_data_sender)
        self.rfid_controller = RfidController.instance(rfid_callback)

        #* Button to send requests
        from button.Button import Button
        button_send_ws_data = ButtonSendWSData(ws_data_sender)
        self.sending_button = Button(ButtonPins.instance().sending_button_number, button_send_ws_data)

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
            # self.run_checks()
            while True:
                if self.ws_client.connected:
                    self.rfid_controller.process()
                    self.sending_button.process()
        except KeyboardInterrupt:
            DLog.Log("End of the program")

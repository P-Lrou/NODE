from GlobalVariables import *
from MyDelegates import *
from tools.DLog import DLog
from tools.LedDisplayer import LedDisplayer
from message.MessageHandler import MessageHandler
from wsclient.WSDelegate import WSDelegate
import RPi.GPIO as GPIO
import sys
import time

class IOTManager(WSDelegate):
    def __del__(self):
        GPIO.cleanup()

    def __init__(self) -> None:
        #* Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        #* Websocket client
        from wsclient.WSClient import WSClient
        self.message_handler = MessageHandler(self)
        self.ws_client = WSClient.connectToVPS(self)

        #* Dock
        from dock.DockController import DockController
        rfid_dock_callback = RfidDockCallback(self.ws_client)
        self.dock_controller = DockController(rfid_dock_callback)

        #* Button
        from button.MyButton import MyButton
        button_callback = ButtonCallback(self.ws_client)
        self.button = MyButton(18, "belotte", button_callback)

    def run_checks(self):
        LedDisplayer.setup()
        LedDisplayer.new_test_sequence()
        if True:  # self.rfid_controller.process_checker():
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
                    self.dock_controller.process()
                    self.button.process()
        except KeyboardInterrupt:
            DLog.Log("End of the program")

    def on_message(self, json_message):
        super().on_message(json_message)
        self.message_handler.process_message(json_message)

    def get_dock_by_activity(self, activity_type: str):
        return self.dock_controller.get_dock_by_activity(activity_type)

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
    def close(self):
        self.dock_controller.stop_all()
        GPIO.cleanup()

    def __init__(self) -> None:
        #* Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        #* Websocket client
        from wsclient.WSClient import WSClient
        self.message_handler = MessageHandler(self)
        self.ws_client = WSClient.connectToVPS(self)
        ws_data_sender = WebSocketDataSender(self.ws_client)
        
        #* Dock
        from dock.DockController import DockController
        rfid_dock_callback = RfidDockCallback(self, ws_data_sender)
        self.dock_controller = DockController(rfid_dock_callback)

        #* Button to send requests
        from button.Button import Button
        button_send_ws_data = ButtonSendWSData(ws_data_sender)
        self.sending_button = Button(ButtonPins.instance().sending_button_number, button_send_ws_data)
        

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
                    self.sending_button.process()
        except KeyboardInterrupt:
            DLog.Log("End of the program")

    def on_message(self, json_message):
        super().on_message(json_message)
        self.message_handler.process_message(json_message)

    def get_dock_by_activity(self, activity_type: str):
        return self.dock_controller.get_docks_by_activity(activity_type)[0]
    
    def get_docks_by_non_activity(self, activity_type: str):
        return self.dock_controller.get_docks_by_non_activity(activity_type)
    
    def get_empty_docks(self):
        return self.dock_controller.get_docks_by_activity("")

    def get_docks(self):
        return self.dock_controller.docks
    
    def has_active_docks(self):
        return self.dock_controller.has_active_dock()
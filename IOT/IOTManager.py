import RPi.GPIO as GPIO
from GlobalVariables import *

#* TOOLS
from tools.DLog import DLog

#* WEBSOCKET
from wsclient.WSDelegate import WSDelegate
from wsclient.WSManager import WSManager
from message.MessageHandler import MessageHandler

#* DOCK
from dock.DockManager import DockManager

#* BUTTON
from button.Button import Button
from button.ButtonDelegate import ButtonDelegate

class IOTManager(WSDelegate, ButtonDelegate):
    def close(self):
        self.dock_manager.stop_all()
        GPIO.cleanup()

    def __init__(self) -> None:
        #* Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        #* Websocket client
        self.message_handler = MessageHandler(self)
        self.ws_manager = WSManager.connect_to_vps(delegate=self)
        
        #* Dock
        self.dock_manager = DockManager(ws_manager=self.ws_manager)

        #* Button to send requests
        self.sending_button = Button(ButtonPins.instance().sending_button_number, delegate=self)

    def start(self):
        try:
            self.ws_manager.start()
            while True:
                if self.ws_manager.is_connected():
                    self.dock_manager.process()
                    self.sending_button.process()
        except KeyboardInterrupt:
            self.dock_manager.stop_all()
            DLog.Log("End of the program")

    def on_message(self, json_message):
        super().on_message(json_message)
        self.message_handler.process_message(json_message)

    def on_clicked(self, button: Button) -> None:
        self.dock_manager.handle_activities()
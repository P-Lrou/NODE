from GlobalVariables import *
from message.MessageHandler import MessageHandler
from tools.DLog import DLog
import json

#* Websocket Client
from wsclient.WSDelegate import WSDelegate

class WSClientCallback(WSDelegate):
    def __init__(self) -> None:
        super().__init__()
        self.message_handler = MessageHandler()

    def on_message(self, json_message):
        super().on_message(json_message)
        self.message_handler.process_message(json_message)


#* Rfid reader
from rfid.RfidDelegate import RfidDelegate

class RfidCallback(RfidDelegate):
    def __init__(self, ws_client=None) -> None:
        super().__init__()
        self.ws_client = ws_client

    def define_activity(self, rfid) -> str:
        if rfid.last_text_read:
            activities: list[str] = Activities.instance().activities
            for activity in activities:
                if rfid.last_text_read.startswith(activity):
                    return activity
            DLog.LogError("Unkown activity")
        else:
            DLog.LogError("No text has been read yet")
        return None
    
    def rfid_placed(self, rfid, rfid_data):
        super().rfid_placed(rfid, rfid_data)
        activity = self.define_activity(rfid)
        DLog.Log(activity)
        if activity:
            if self.ws_client is not None:
                data = {
                    "type": "activity",
                    "activity_type": activity,
                    "state": "request"
                }
                self.ws_client.send_message(json.dumps(data))
            else:
                DLog.LogError("Fail to send message")

    def rfid_removed(self, rfid):
        super().rfid_removed(rfid)
        activity = self.define_activity(rfid)
        DLog.Log(activity)
        if activity:
            if self.ws_client is not None:
                data = {
                    "type": "activity",
                    "activity_type": activity,
                    "state": "retire"
                }
                self.ws_client.send_message(json.dumps(data))
            else:
                DLog.LogError("Fail to send message")


#* Rfid reader
from button.ButtonDelegate import ButtonDelegate

class ButtonCallback(ButtonDelegate):
    def __init__(self, ws_client=None) -> None:
        super().__init__()
        self.ws_client = ws_client

    def on_clicked(self, button) -> None:
        super().on_clicked(button)
        self.ws_client.send_message(json.dumps(button.get_data()))
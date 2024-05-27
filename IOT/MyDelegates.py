from GlobalVariables import *
from message.MessageHandler import MessageHandler
from tools.DLog import DLog
from tools.Timer import Timer
from tools.JSONTools import *

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
        self.timeout_request_seconds = 10

    def __send_data(self, data, is_last: bool = False):
        if self.ws_client:
            if data:
                data["is_last"] = is_last
                message = json_encode(data)
                if message:
                    self.ws_client.send_message(message)
            else:
                DLog.LogError("There is no data to send")
        else:
            DLog.LogError("Fail to send message")

    def __get_request_data(self, activity):
        data = {
            "type": "activity",
            "activity_type": activity,
            "state": "request"
        }
        return data

    def define_activity(self, rfid) -> str:
        if rfid.last_text_read is not None:
            if len(rfid.last_text_read) != 0:
                activities: list[str] = Activities.instance().activities
                for activity in activities:
                    if rfid.last_text_read.startswith(activity):
                        return activity
                DLog.LogError(f"Unkown activity. Text: {rfid.last_text_read}")
            else:
                DLog.LogError("Erreur pour retirer le badge")
                #TODO: VOIR AVEC LES DESIGNER SI JE COUPE LE TIMER OU NON
        else:
            DLog.LogError("No text has been read yet")
        return None
    
    def rfid_placed(self, rfid, rfid_data):
        super().rfid_placed(rfid, rfid_data)
        activity = self.define_activity(rfid)
        if activity is not None:
            DLog.Log(f"{activity} placed")
            data = self.__get_request_data(activity)
            Timer.instance().start(self.timeout_request_seconds, self.__send_data, data)


    def rfid_removed(self, rfid):
        super().rfid_removed(rfid)
        activity = self.define_activity(rfid)
        if activity is not None:
            DLog.Log(f"{activity} removed")
            if Timer.instance().is_running():
                Timer.instance().pop_callback(self.__send_data, self.__get_request_data(activity))
            else:
                data = {
                    "type": "activity",
                    "activity_type": activity,
                    "state": "cancel"
                }
                self.__send_data(data)


#* Rfid reader
from button.ButtonDelegate import ButtonDelegate

class ButtonCallback(ButtonDelegate):
    def __init__(self, ws_client=None) -> None:
        super().__init__()
        self.ws_client = ws_client

    def on_clicked(self, button) -> None:
        super().on_clicked(button)
        self.ws_client.send_message(json_encode(button.get_data()))
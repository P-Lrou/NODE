from GlobalVariables import *
from tools.DLog import DLog
from tools.JSONTools import *
from wsclient.WebSocketDataSender import WebSocketDataSender

#* Rfid reader
from rfid.RfidDelegate import RfidDelegate

class RfidDockCallback(RfidDelegate):
    def __init__(self, parent = None, ws_data_sender: WebSocketDataSender = None) -> None:
        super().__init__()
        self.ws_data_sender = ws_data_sender
        self.parent = parent
        self.timeout_request_seconds = 10
        self.dock = None

    def __send_data(self, is_safe: bool = False):
        if self.ws_data_sender:
            self.ws_data_sender.send_data(is_safe)
        else:
            DLog.LogError("There is no websocket data sender")

    def __add_data(self, data):
        if self.ws_data_sender:
            if data:
                self.ws_data_sender.new_data(data)
            else:
                DLog.LogError("There is no data to send")
        else:
            DLog.LogError("There is no websocket data sender")

    def __remove_data(self, data):
        if self.ws_data_sender:
            if data:
                return self.ws_data_sender.remove_data(data)
            else:
                DLog.LogError("There is no data to remove")
        else:
            DLog.LogError("There is no websocket data sender")
        return False

    def __get_request_data(self, activity: str):
        data = {
            "type": "activity",
            "activity_type": activity,
            "state": "request"
        }
        return data
    
    def __get_cancel_data(self, activity: str):
        data = {
            "type": "activity",
            "activity_type": activity,
            "state": "cancel"
        }
        return data

    def define_activity(self, rfid) -> str:
        if rfid.last_text_read is not None:
            if len(rfid.last_text_read) != 0:
                data: list[str] = rfid.last_text_read.split(":")
                activity_type = ""
                color_name = ""
                if len(data) > 1:
                    activity_type = data[0]
                    color_name = data[1]
                else:
                    activity_type = data[0]
                activities: list[str] = Activities.instance().activities
                for activity in activities:
                    if activity_type == activity:
                        return activity, color_name
                DLog.LogError(f"Unkown activity. Text: '{rfid.last_text_read}'")
            else:
                DLog.LogError("Erreur pour retirer le badge")
                #TODO: VOIR AVEC LES DESIGNER SI JE COUPE LE TIMER OU NON // ATTENTION IL Y A PLUS DE TIMER
        else:
            DLog.LogError("No text has been read yet")
        return None, None
    
    def rfid_placed(self, rfid, rfid_data):
        super().rfid_placed(rfid, rfid_data)
        activity, color = self.define_activity(rfid)
        if activity is not None:
            DLog.Log(f"{activity} placed")
            dock = rfid.parent
            if dock is not None:
                dock.activity = activity
                dock.color_name = color
                dock.launch_fill()
                docks = self.parent.get_empty_docks()
                for non_dock in docks:
                    non_dock.launch_wait()
                # PlaySound.join()
                # PlaySound.play_sound(dock.sounds["rfid"]["placed"])
            self.__remove_data(self.__get_cancel_data(activity))
            self.__add_data(self.__get_request_data(activity))


    def rfid_removed(self, rfid):
        super().rfid_removed(rfid)
        activity, color = self.define_activity(rfid)
        if activity is not None:
            DLog.Log(f"{activity} removed")
            dock = rfid.parent
            dock.activity = ""
            dock.color_name = ""
            if not self.parent.has_active_docks():
                docks = self.parent.get_docks()
                for non_dock in docks:
                    non_dock.launch_stop()
            else:
                dock = rfid.parent.launch_wait()
            if not self.__remove_data(self.__get_request_data(activity)):
                self.__add_data(self.__get_cancel_data(activity))
                self.__send_data(True)
            else:
                self.__add_data(self.__get_cancel_data(activity))



#* Rfid reader
from button.ButtonDelegate import ButtonDelegate

class ButtonSendWSData(ButtonDelegate):
    def __init__(self, ws_data_sender: WebSocketDataSender = None) -> None:
        super().__init__()
        self.ws_data_sender = ws_data_sender

    def on_clicked(self, button) -> None:
        super().on_clicked(button)
        self.ws_data_sender.send_data()
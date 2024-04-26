from GlobalVariables import *

#* Websocket Client
from wsclient.WSDelegate import WSDelegate

class WSClientCallback(WSDelegate):
    def __init__(self) -> None:
        super().__init__()

    def on_message(self, json_message):
        super().on_message(json_message)


#* Rfid reader
from rfid.RfidDelegate import RfidDelegate

class RfidCallback(RfidDelegate):
    def __init__(self, ws_client=None) -> None:
        super().__init__()
        self.ws_client = ws_client
    
    def rfid_placed(self, rfid_data):
        super().rfid_placed(rfid_data)
        activities = Activities.instance.activities
        if rfid_data["text"] in activities:
            for activity in activities:
                if rfid_data["text"].startsWith(activity):
                    if self.ws_client is None:
                        self.ws_client.send_message(activity)
                    else:
                        print("Error: Fail to send message")
                    break

    def rfid_removed(self):
        super().rfid_removed()

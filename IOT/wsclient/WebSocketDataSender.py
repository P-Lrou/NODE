from tools.JSONTools import *
from tools.DLog import DLog

class WebSocketDataSender:
    def __init__(self, ws_client) -> None:
        self.ws_client = ws_client
        self.data: list[dict] = []

    def new_data(self, new_data: dict):
        self.data.append(new_data)

    def remove_data(self, pop_data: dict):
        for key, data in enumerate(self.data):
            if data == pop_data:
                self.data.pop(key)
                return True
        return False
    
    def send_data(self, is_safe: bool = False):
        if not is_safe or (is_safe and len(self.data) < 2):
            for key, data in enumerate(self.data):
                data["is_last"] = (key == len(self.data) - 1)
                str_data = json_encode(data)
                if str_data:
                    self.ws_client.send_message(json_encode(data))
            self.data = []


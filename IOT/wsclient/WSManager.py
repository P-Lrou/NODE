from tools.JSONTools import *
from tools.Timer import Timer
from wsclient.WSClient import WSClient
from wsclient.WSDelegate import WSDelegate

class WSManager:
    def __init__(self, uri, delegate: WSDelegate = None) -> None:
        self.ws_client = WSClient(uri, delegate)
        self.interval_retrying = 5

    def start(self) -> bool:
        self.ws_client.start()

    def is_connected(self) -> bool:
        return self.ws_client.connected
    
    def __send_message(self, data) -> None:
        if self.is_connected():
            self.ws_client.send_message(json_encode(data))
        else:
            Timer().start(self.interval_retrying, self.ws_client.send_message, json_encode(data))
    
    def send_activities_request(self, activities_type: list[str]) -> None:
        data = {
            "type": "activity",
            "activities_type": activities_type,
            "state": "request"
        }
        self.__send_message(data)

    def send_activities_cancel(self, activities_type: list[str]) -> None:
        data = {
            "type": "activity",
            "activities_type": activities_type,
            "state": "cancel"
        }
        self.__send_message(data)

    @classmethod
    def connect_to_vps(cls, delegate: WSDelegate = None) -> "WSManager":
        uri = "ws://{ip}:{port}".format(
            ip="websocket.rezurrection.website", port=8765)
        return cls(uri, delegate)
    
    @classmethod
    def connect_to_localhost(cls, delegate: WSDelegate = None) -> "WSManager":
        uri = "ws://{ip}:{port}".format(ip="localhost", port=9000)
        return cls(uri, delegate)
    

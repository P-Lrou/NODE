from wsclient.WSClient import WSClient
from wsclient.WSDelegate import WSDelegate
from ActivitySimulation import ActivitySimulation
import time, json

class MyDelegate(WSDelegate):
    def __init__(self, data_to_send:list[str] = [], sending_delta:int = 10) -> None:
        super().__init__()
        self.ws_client = None
        self.has_sending = False
        self.data_to_send = data_to_send
        self.sending_delta = sending_delta

    def set_ws_client(self, ws_client):
        self.ws_client = ws_client

    def on_open(self):
        super().on_open()

    def on_message(self, message):
        super().on_message(message)
        if not self.has_sending:
            self.has_sending = True
            for data in data_to_send:
                self.ws_client.send_message(data)
                time.sleep(self.sending_delta)

    def on_close(self):
        super().on_close()

    def on_error(self, error):
        super().on_error(error)

data_to_send = [
    ActivitySimulation.add_belote()
]
my_delegate = MyDelegate(data_to_send)
# client = WSClient.connectToLocalhost(my_delegate)
client = WSClient.connectToVPS(my_delegate)
my_delegate.set_ws_client(client)
client.start()

from wsclient.WSClient import WSClient
from wsclient.WSDelegate import WSDelegate
from ActivitySimulation import ActivitySimulation
import time, json

class MyDelegate(WSDelegate):
    def __init__(self) -> None:
        super().__init__()
        self.ws_client = None
        self.all_received = False

    def set_ws_client(self, ws_client):
        self.ws_client = ws_client

    def on_open(self):
        super().on_open()

    def on_message(self, message):
        super().on_message(message)
        try:
            data = message
            if "uid" in data:
                self.send_first_data()
                pass
            if "type" in data:
                self.send_second_data()
                pass
        except:
            pass

    def on_close(self):
        super().on_close()

    def on_error(self, error):
        super().on_error(error)

    def send_first_data(self):
        if self.ws_client:
            self.ws_client.send_message(
                ActivitySimulation.add_tarot()
            )
    def send_second_data(self):
        time.sleep(10)
        if self.ws_client and not self.all_received:
            self.ws_client.send_message(
                ActivitySimulation.remove_tarot()
            )
            self.all_received = True

my_delegate = MyDelegate()
client = WSClient.connectToVPS(my_delegate)
my_delegate.set_ws_client(client)
client.start()
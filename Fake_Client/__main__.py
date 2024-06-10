from wsclient.WSClient import WSClient
from wsclient.WSDelegate import WSDelegate
from ActivitySimulation import ActivitySimulation
import time, json

class MyDelegate(WSDelegate):
    def __init__(self, data:dict = {}, sending_delta:int = 10) -> None:
        super().__init__()
        self.ws_client = None
        self.has_sending = False
        self.data = data
        self.sending_delta = sending_delta

    def set_ws_client(self, ws_client):
        self.ws_client = ws_client

    def on_open(self):
        super().on_open()

    def on_message(self, message):
        super().on_message(message)
        if not self.has_sending:
            self.has_sending = True
            if self.data:
                self.ws_client.send_message(json.dumps(self.data))
                time.sleep(self.sending_delta) #! TIMING
                # self.ws_client.send_message(json.dumps(ActivitySimulation.remove([ActivitySimulation.GOUTER])))

    def on_close(self):
        super().on_close()

    def on_error(self, error):
        super().on_error(error)

#! ATTENTION SI PLUSIEURS DATA TO SEND => UN TIME.SLEEP EST EFFECTUE
data = ActivitySimulation.add([
        ActivitySimulation.GOUTER
    ]
)

my_delegate = MyDelegate(data)
# client = WSClient.connectToLocalhost(my_delegate)
client = WSClient.connectToVPS(my_delegate)
my_delegate.set_ws_client(client)
client.start()
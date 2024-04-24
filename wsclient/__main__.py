from WSClient import WSClient
from WSDelegate import WSDelegate

class MyDelegate(WSDelegate):
    def __init__(self) -> None:
        super().__init__()

    def on_open(self):
        super().on_open()

    def on_message(self, message):
        super().on_message(message)

    def on_close(self):
        super().on_close()

    def on_error(self, error):
        super().on_error(error)

my_delegate = MyDelegate()
client = WSClient.connectToVPS(my_delegate)
client.start()
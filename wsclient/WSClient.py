import websocket
from threading import Thread

class WSClient(Thread):
    def __init__(self, uri, delegate=None):
        super().__init__()
        self.uri = uri
        self.delegate = delegate
        self.ws = websocket.WebSocketApp(uri,
                                         on_open=self.on_open,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.connected = False
        self.time_ms_error = 2000

    def run(self):
        self.ws.run_forever()

    def send_message(self, message):
        self.ws.send(message)

    def on_open(self, ws):
        self.connected = True
        if self.delegate:
            self.delegate.on_open()

    def on_message(self, ws, message):
        if self.delegate:
            self.delegate.on_message(message)

    def on_error(self, ws, error):
        if self.delegate:
            self.delegate.on_error(ws, error)

    def on_close(self, ws):
        self.connected = False
        if self.delegate:
            self.delegate.on_close()

    @staticmethod
    def connectToVPS(delegate=None):
        uri = "ws://{ip}:{port}".format(ip="websocket.rezurrection.website", port=8765)
        return WSClient(uri, delegate)
import websocket
from threading import Thread
from tools.JSONTools import *
from tools.DLog import DLog

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
        self.uid = None

    def run(self):
        self.ws.run_forever()

    def send_message(self, text):
        message = {
            "uid": self.uid,
            "text": text
        }
        DLog.LogWhisper(f"Sending message: {message}")
        message_to_send = json_encode(message)
        if message_to_send:
            self.ws.send(message_to_send)

    def on_open(self, ws):
        self.connected = True
        if self.delegate:
            self.delegate.on_open()

    def on_message(self, ws, message):
        json_message = json_decode(message)
        if json_message:
            if "uid" in json_message:
                self.uid = json_message["uid"]
            if self.delegate:
                self.delegate.on_message(json_message)

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

    @staticmethod
    def connectToLocalhost(delegate=None):
        uri = "ws://{ip}:{port}".format(ip="localhost", port=9000)
        return WSClient(uri, delegate)
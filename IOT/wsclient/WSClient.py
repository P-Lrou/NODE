import websocket
from threading import Thread, Event
import json
import time

class WSClient(Thread):
    def __init__(self, uri, delegate=None):
        super().__init__()
        self.uri = uri
        self.delegate = delegate
        self.connected = False
        self.uid = None
        self.stop_event = Event()
        self.ws = websocket.WebSocketApp(uri,
                                         on_open=self.on_open,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)

    def run(self):
        self.ws.run_forever()

    def send_message(self, text):
        if self.connected:
            message = {
                "uid": self.uid,
                "text": text
            }
            print(f"Sending message: {message}")
            self.ws.send(json.dumps(message))
        else:
            print("Cannot send message, not connected")

    def on_open(self, ws):
        self.connected = True
        if self.uid is not None:
            self.send_message(f"uid:{self.uid}")
        if self.delegate:
            self.delegate.on_open()

    def on_message(self, ws, message):
        json_message = json.loads(message)
        if "uid" in json_message and self.uid is not None:
            self.uid = json_message["uid"]
        if self.delegate:
            self.delegate.on_message(json_message)

    def on_error(self, ws, error):
        if self.delegate:
            self.delegate.on_error(ws, error)

    def on_close(self, ws, close_status_code, close_msg):
        self.connected = False
        if self.delegate:
            self.delegate.on_close()

        while not self.connected and not self.stop_event.is_set():
            try:
                self.ws = websocket.WebSocketApp(self.uri,
                                                 on_open=self.on_open,
                                                 on_message=self.on_message,
                                                 on_error=self.on_error,
                                                 on_close=self.on_close)
                self.ws.run_forever()
            except Exception as e:
                print(f"Reconnection failed: {e}")
            time.sleep(5)

    def stop(self):
        self.stop_event.set()
        if self.ws:
            self.ws.close()

    @staticmethod
    def connectToVPS(delegate=None):
        uri = "ws://{ip}:{port}".format(
            ip="websocket.rezurrection.website", port=8765)
        return WSClient(uri, delegate)

    @staticmethod
    def connectToLocalhost(delegate=None):
        uri = "ws://{ip}:{port}".format(ip="localhost", port=9000)
        return WSClient(uri, delegate)

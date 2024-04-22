from tools.DLog import DLog
from websocket_server import WebsocketServer


class WSServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def handle_message(self, client, server, message):
        DLog.Log(f"Received message from {client['id']}: {message}")
        response = f"Echo: {message}"
        server.send_message(client, response)
        DLog.Log(f"Sent response to {client['id']}: {response}")

    def start(self):
        DLog.LogSuccess(f"Server starting at ws://{self.host}:{self.port}")
        server = WebsocketServer(self.port, host=self.host)
        server.set_fn_message_received(self.handle_message)
        server.run_forever()
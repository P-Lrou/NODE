from tools.DLog import DLog
from Message.MessageHandler import MessageHandler
from websocket_server import WebsocketServer
import json
import uuid


class WSServer:
    def __init__(self, host, port, delegate=None):
        self.host = host
        self.port = port
        self.current_users = []
        self.delegate = delegate
        self.server = None

    def handle_new_connection(self, client, server):
        uid = str(uuid.uuid4())
        while any(user['uid'] == uid for user in self.current_users):
            uid = str(uuid.uuid4())
        self.current_users.append({"client": client['id'], "uid": uid})
        client['uid'] = uid
        welcome_message = json.dumps({"uid": uid})
        DLog.LogWhisper(f"New Client : {uid}")
        server.send_message(client, welcome_message)
        if self.delegate:
            self.delegate.new_connection(client, server)

    def handle_client_left(self, client, server):
        for index in range(0, len(self.current_users)):
            if self.current_users[index]["client"] == client['id']:
                DLog.LogWarning(f"Client {client['id']} -> {self.current_users[index]['uid']} disconnected")
                self.current_users.pop(index)
                if self.delegate:
                    self.delegate.lose_connection(client, server)
                return
        DLog.LogWarning(f"Client {client['id']} disconnected")

    def handle_message(self, client, server, message):
        DLog.Log(f"Received message from {client['id']}: {message}")
        if self.delegate:
            self.delegate.received_message(client, server, message)

    def start(self):
        DLog.LogSuccess(f"Server starting at ws://{self.host}:{self.port}")
        self.server = WebsocketServer(port=self.port, host=self.host)
        self.server.set_fn_new_client(self.handle_new_connection)
        self.server.set_fn_message_received(self.handle_message)
        self.server.set_fn_client_left(self.handle_client_left)
        self.server.run_forever()

    def send_messages(self, messages):
        self.delegate.send_messages(self.server, messages)

    @staticmethod
    def setupVPS(delegate=None):
        return WSServer('websocket.rezurrection.website', 8765, delegate)

    @staticmethod
    def setupLocalhost(delegate=None):
        return WSServer('localhost', 9000, delegate)
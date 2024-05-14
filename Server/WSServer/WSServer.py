from tools.DLog import DLog
from Message.MessageHandler import MessageHandler
from websocket_server import WebsocketServer
import json
import uuid


class WSServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.current_users = []
        self.messageHandler = MessageHandler()

    def handle_new_connection(self, client, server):
        uid = str(uuid.uuid4())
        while any(user['uid'] == uid for user in self.current_users):
            uid = str(uuid.uuid4())
        self.current_users.append({"client": client['id'], "uid": uid})
        client['uid'] = uid
        welcome_message = json.dumps({"uid": uid})
        DLog.LogWhisper(f"New Client : {uid}")
        server.send_message(client, welcome_message)

    def handle_client_left(self, client, server):
        for index in range(0, len(self.current_users)):
            if self.current_users[index]["client"] == client['id']:
                DLog.LogWarning(
                    f"Client {client['id']} -> {self.current_users[index]['uid']} disconnected")
                self.current_users.pop(index)
                self.messageHandler.process_disconnection(server, client)
                return
        DLog.LogWarning(f"Client {client['id']} disconnected")
    def handle_message(self, client, server, message):
        DLog.Log(f"Received message from {client['id']}: {message}")
        self.messageHandler.process_message(message, server, client)

    def start(self):
        DLog.LogSuccess(f"Server starting at ws://{self.host}:{self.port}")
        server = WebsocketServer(port=self.port, host=self.host)
        server.set_fn_new_client(self.handle_new_connection)
        server.set_fn_message_received(self.handle_message)
        server.set_fn_client_left(self.handle_client_left)
        server.run_forever()

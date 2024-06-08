from tools.DLog import DLog
from tools.JSONTools import *
from Checker.Testable import Testable
from websocket_server import WebsocketServer
import uuid
import time


class WSServer(Testable):
    def __init__(self, host, port, delegate=None):
        self.host = host
        self.port = port
        self.current_users = []
        self.delegate = delegate
        self.server = None
        self.test_timeout_seconds = 3

    def handle_new_connection(self, client, server):
        DLog.LogWhisper(f"New Client!")
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

    def handle_message(self, client, server, message: str):
        DLog.Log(f"Received message from {client['id']}: {message}")
        data_message = json_decode(message)
        if data_message:
            if "uid" in data_message:
                if data_message["uid"] == None:
                    uid = str(uuid.uuid4())
                    self.current_users.append({"client": client['id'], "uid": uid})
                    client['uid'] = uid
                    welcome_message = json_encode({"uid": uid})
                    DLog.LogWhisper(f"New Client : {uid}")
                    server.send_message(client, welcome_message)
                    if self.delegate:
                        self.delegate.new_client(uid)
                else:
                    uid = data_message["uid"]
                    client["uid"] = uid
                    if self.delegate:
                        self.delegate.client_reconnected(uid)
        if self.delegate:
            self.delegate.received_message(client, server, message)

    def start(self):
        DLog.Log(f"Server starting at ws://{self.host}:{self.port}")
        try:
            self.server = WebsocketServer(port=self.port, host=self.host)
            self.server.set_fn_new_client(self.handle_new_connection)
            self.server.set_fn_message_received(self.handle_message)
            self.server.set_fn_client_left(self.handle_client_left)
            self.server.run_forever()
        except Exception as e:
            DLog.LogError(f"Failed to start WebSocket server: {e}")

    def shutdown_gracefully(self):
        if self.server:
            DLog.Log("Shutting down WebSocket server gracefully...")
            self.server._disconnect_clients_gracefully()
            self.server._shutdown_gracefully()
            DLog.Log("WebSocket server shut down.")
        else:
            DLog.LogWarning("There is no server to shutdown")

    @staticmethod
    def setup_VPS(delegate=None):
        return WSServer('websocket.rezurrection.website', 8765, delegate)

    @staticmethod
    def setup_localhost(delegate=None):
        return WSServer('localhost', 9000, delegate)
    
    @staticmethod
    def setup_crash(delegate=None):
        return WSServer('52.37.177.190', 9000, delegate)
    
    def test(self):
        actual_time = 0
        while actual_time <= self.test_timeout_seconds:
            if self.server:
                return True
            time.sleep(0.1)
            actual_time += 0.1
        return False
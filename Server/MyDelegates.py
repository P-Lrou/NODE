# TOOLS
from tools.DLog import DLog
from tools.JSONTools import *
# WEBSOCKET SERVER
from WSServer.WSServerDelegate import WSServerDelegate
from WSServer.ClientHandler import ClientHandler
# CLIENT MODEL
from Model.Client import Client
from Model.Request import Request

class WSServerCallback(WSServerDelegate):
    def __init__(self) -> None:
        super().__init__()
        self.client_handler = ClientHandler()

    def new_connection(self, client, server) -> None:
        super().new_connection(client, server)

    def new_client(self, uid) -> None:
        new_client = Client.insert(uid)
        if new_client:
            DLog.LogSuccess("Insert client")
        else:
            DLog.LogError(f"Fail to insert client with uid: {uid}")

    def client_reconnected(self, uid) -> None:
        client: Client = Client.get_first_client_by_uid(uid)
        if client:
            requests = client.get_disconnected_requests()
            for request in requests:
                request.update_state(Request.ATTEMPTING)
        else:
            DLog.LogError(f"No client found with uid: {uid}")

    def received_message(self, client, server, message: str) -> None:
        super().received_message(client, server, message)
        data_message = json_decode(message)
        if data_message:
            if "uid" not in data_message:
                DLog.LogError("There is not 'uid' key in this message")
                server.send_message(client, json_encode({"error": "There is not 'uid' key in this message"}))
                return

            if "text" not in data_message:
                DLog.LogError("There is not 'text' key in this message")
                server.send_message(client, json_encode({"error": "There is not 'text' key in this message"}))
                return
            
            data = json_decode(data_message["text"])
            if data:
                data["client_id"] = client["id"]
                data["client_uid"] = client["uid"]
                data_to_send = self.client_handler.process_message(data)
                if isinstance(data_to_send, dict):
                    server.send_message(client, json_encode(data_to_send))
                else:
                    self.send_messages(server, data_to_send)
            

    def lose_connection(self, client, server) -> None:
        super().lose_connection(client, server)
        self.client_handler.process_disconnection(client)

    def send_data(self, server, data):
        if "targets" in data:
            if "message" in data:
                if data["targets"] == "all":
                    DLog.LogWhisper(f"sending => {data['message']}")
                    for client in server.clients:
                        server.send_message(client, data["message"])
                else:
                    for uid in data["targets"]:
                        DLog.LogWhisper(f"sending => {data['message']}")
                        for client in server.clients:
                            if client["uid"] == uid:
                                server.send_message(client, data["message"])
            else:
                DLog.LogError("No 'message' key in data")
        else:
            DLog.LogError("No 'targets' key in data")

    def send_messages(self, server, data_to_send: list) -> None:
        for non_typed_data in data_to_send:
            if isinstance(non_typed_data, list):
                for data in non_typed_data:
                    self.send_data(server, data)
            else:
                self.send_data(server, non_typed_data)
                

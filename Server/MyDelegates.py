# TOOLS
from tools.DLog import DLog
from tools.JSONManager import *
# WEBSOCKET SERVER
from WSServer.WSServerDelegate import WSServerDelegate
from WSServer.ClientHandler import ClientHandler

class WSServerCallback(WSServerDelegate):
    def __init__(self) -> None:
        super().__init__()
        self.client_handler = ClientHandler()

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
        messages = self.client_handler.process_disconnection(client)
        self.send_messages(messages)

    def send_messages(self, server, data_to_send: list[dict]) -> None:
        for data in data_to_send:
            if "tagrets" in  data:
                if "message" in data:
                    if data["targets"] == "all":
                        for client in server.clients:
                            server.send_message(client, data["message"])
                    else:
                        for id in data["targets"]:
                            for client in server.clients:
                                if client["id"] == id:
                                    server.send_message(client, data["message"])
                else:
                    DLog.LogError("No 'message' key in data")
            else:
                DLog.LogError("No 'targets' key in data")

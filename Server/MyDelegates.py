from WSServer.WSServerDelegate import WSServerDelegate
from ClientHandler import ClientHandler
from tools.DLog import DLog
from tools.JSONManager import *

class WSServerCallback(WSServerDelegate):
    def __init__(self) -> None:
        super().__init__()
        self.client_handler = ClientHandler()

    def received_message(self, client, server, message:str) -> None:
        super().received_message(client, server, message)
        data_message = json_encode(message)
        if data_message:
            if "uid" not in data_message:
                DLog.LogError("There is not 'uid' key in this message")
                server.send_message(client, json.dumps({"error": "There is not 'uid' key in this message"}))
                return

            if "text" not in data_message:
                DLog.LogError("There is not 'text' key in this message")
                server.send_message(client, json.dumps({"error": "There is not 'text' key in this message"}))
                return
            
            data = json_decode(data_message["text"])
            if data:
                data["client_id"] = client["id"]
                data["client_uid"] = client["uid"]
                messages = self.client_handler.process_message(data)
                self.send_messages(messages)
            

    def lose_connection(self, client, server) -> None:
        super().lose_connection(client, server)
        messages = self.client_handler.process_disconnection(client)
        self.send_messages(messages)

    def send_messages(self, server, messages) -> None:
        for message in messages:
            if message["targets"] == "all":
                for client in server.clients:
                    server.send_message(client, message["message"])
            else:
                for id in message["targets"]:
                    for client in server.clients:
                        if client["id"] == id:
                            server.send_message(client, message["message"])

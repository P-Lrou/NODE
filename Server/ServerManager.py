from tools.DLog import DLog
from MyDelegates import *
from Activities.ActivitiesManager import ActivitiesManager
import threading

class ServerManager:
    def __init__(self) -> None:
        #* Setup Client Handler
        from ClientHandler import ClientHandler
        self.client_handler = ClientHandler()

        #* Setup Websocket Server
        from WSServer.WSServer import WSServer
        ws_server_delegate = WSServerCallback(self.client_handler)
        self.ws_server: WSServer = WSServer.setupLocalhost(ws_server_delegate)
        # self.ws_server = WSServer.setupVPS(ws_server_delegate)
        self.server_thread = threading.Thread(target=self.ws_server.start)

    def start(self) -> None:
        self.server_thread.start()
        try:
            while True:
                if self.ws_server.server is not None:
                    ActivitiesManager.check_room_waiting_time(self.ws_server.send_messages)
        except KeyboardInterrupt:
             DLog.Log("End of the program")
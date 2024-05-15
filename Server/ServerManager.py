from tools.DLog import DLog
from MyDelegates import *
from Activities.ActivitiesManager import ActivitiesManager
import threading

class ServerManager:
    def __del__(self):
        self.stop()

    def __init__(self) -> None:

        #* Setup Websocket Server
        from WSServer.WSServer import WSServer
        self.ws_server_delegate = WSServerCallback()
        self.ws_server: WSServer = WSServer.setup_localhost(self.ws_server_delegate)
        # self.ws_server = WSServer.setup_VPS(ws_server_delegate)
        self.server_thread = threading.Thread(target=self.ws_server.start)
        self.stop_event = threading.Event()  # Event to signal the thread to stop

    def start(self) -> None:
        self.server_thread.start()
        try:
            while not self.stop_event.is_set():
                if self.ws_server.server is not None:
                    ActivitiesManager.check_room_waiting_time(self.ws_server_delegate.send_messages)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        DLog.Log("Stopping server manager...")
        self.stop_event.set()  # Signal the manager to stop
        self.ws_server.shutdown_gracefully()  # Stop the WebSocket server
        self.server_thread.join()  # Wait for the thread to finish
        DLog.LogSuccess("Server manager stopped.")
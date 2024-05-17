from tools.DLog import DLog
from MyDelegates import *
from Checker.Checker import Checker
from Checker.Testable import Testable
from Checker.DisplayError import DisplayError
import threading

class ServerManager:
    def __del__(self):
        self.stop()

    def __init__(self) -> None:

        #* Setup Websocket Server
        from WSServer.WSServer import WSServer
        self.ws_server_delegate = WSServerCallback()
        # self.ws_server: WSServer = WSServer.setup_crash(self.ws_server_delegate)
        # self.ws_server: WSServer = WSServer.setup_localhost(self.ws_server_delegate)
        self.ws_server = WSServer.setup_VPS(self.ws_server_delegate)
        self.server_thread = threading.Thread(target=self.ws_server.start)
        self.stop_event = threading.Event()  # Event to signal the thread to stop

        from Activities.ActivitiesManager import ActivitiesManager
        self.activity_manager = ActivitiesManager()

        self.testable_objects: list[Testable] = [
            self.ws_server,
            self.activity_manager
        ]
        


    def start(self) -> None:
        self.server_thread.start()
        object_in_error = Checker.test_objects(self.testable_objects)
        if object_in_error:
            DisplayError.display_error(object_in_error)
        else:
            self.activity_manager.reset_database()
            DLog.LogSuccess("Server manager launches correctly")
            try:
                while not self.stop_event.is_set():
                    if self.ws_server.server is not None:
                        self.activity_manager.check_room_waiting_time(self.ws_server_delegate.send_messages)
            except KeyboardInterrupt:
                pass

    def stop(self):
        DLog.Log("Stopping server manager...")
        self.stop_event.set()  # Signal the manager to stop
        self.ws_server.shutdown_gracefully()  # Stop the WebSocket server
        self.server_thread.join()  # Wait for the thread to finish
        DLog.LogSuccess("Server manager stopped.")
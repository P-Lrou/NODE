from WSServer.WSServer import WSServer
from tools.DLog import DLog
import threading

class WSManager:
    def __init__(self, host='localhost', port=8765):
        self.server = WSServer(host, port)

    def start(self, threaded=False):
        if threaded:
            thread = threading.Thread(target=self.server.start)
            thread.daemon = True
            thread.start()
            DLog.LogWhisper("Server started in a new thread.")
        else:
            self.server.start()

    @staticmethod
    def setupVPS():
        return WSManager('websocket.rezurrection.website', 8765)

    @staticmethod
    def setupLocalhost():
        return WSManager('localhost', 9000)
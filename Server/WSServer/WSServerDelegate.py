class WSServerDelegate:
    def __init__(self) -> None:
        pass

    def new_connection(self, client, server) -> None:
        pass

    def lose_connection(self, client, server) -> None:
        pass

    def received_message(self, client, server, message:str) -> None:
        pass
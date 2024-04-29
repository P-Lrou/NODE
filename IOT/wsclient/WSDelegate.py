class WSDelegate:
    def on_open(self):
        print("Connection opened")
        pass

    def on_message(self, json_message):
        print(f"Message received: {json_message}")
        pass

    def on_error(self, error):
        print(f"An error occur: {error}")
        pass

    def on_close(self):
        print("Connection closed")
        pass
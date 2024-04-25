class RfidDelegate:
    def __init__(self) -> None:
        pass

    def rfid_placed(self, rfid_data):
        pass

    def rfid_removed(self):
        pass

    def rfid_detected(self, rfid_data):
        pass

    def rfid_not_detected(self):
        pass

    def rfid_has_written(self, text):
        pass

    def rfid_not_written(self):
        pass
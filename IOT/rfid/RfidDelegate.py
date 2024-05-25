class RfidDelegate:
    def __init__(self) -> None:
        pass

    def rfid_placed(self, rfid, rfid_data):
        pass

    def rfid_removed(self, rfid):
        pass

    def rfid_detected(self, rfid, rfid_data):
        pass

    def rfid_not_detected(self, rfid):
        pass

    def rfid_has_written(self, rfid, text):
        pass

    def rfid_not_written(self, rfid):
        pass
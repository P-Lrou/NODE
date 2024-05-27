from rfid.Rfid import Rfid
from GlobalVariables import RfidPins
import time

class RfidController:
    _instance = None

    def __init__(self, rfid_callback) -> None:
        self.rfid_callback = rfid_callback
        self.rfids: list[Rfid] = [Rfid(pin, self.rfid_callback) for pin in RfidPins.instance().rfid_number]

    @classmethod
    def instance(cls, rfid_callback = None) -> "RfidController":
        if cls._instance is None:
            cls._instance = cls(rfid_callback)
        return cls._instance

    def process(self): 
        for rfid in self.rfids:
            rfid.process()
            time.sleep(0.001)

    def get_rfid_id_by_text(self, text: str) -> str:
        for rfid in self.rfids:
            if rfid.last_text_read is not None and rfid.last_text_read.startswith(text):
                return str(rfid.pin)
        return None

    def process_checker(self):
        return True
        for rfid in self.rfids:
            if not rfid.process_checker():
                return False
        return True
from rfid.Rfid import Rfid
from MyDelegates import RfidCallback
from GlobalVariables import RfidPins
import time

class RfidController:
    def __init__(self, rfid_callback) -> None:
        self.rfid_callback = rfid_callback
        self.rfids: list[Rfid] = [Rfid(pin, self.rfid_callback) for pin in RfidPins.instance().rfid_number]

    def process(self): 
        for rfid in self.rfids:
            rfid.process()
            time.sleep(0.001)

    def process_checker(self):
        return True
        for rfid in self.rfids:
            if not rfid.process_checker():
                return False
        return True
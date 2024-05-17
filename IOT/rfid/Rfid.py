from rfid.mfrc522 import SimpleMFRC522
from checker.CheckerInterface import CheckerInterface
import time

class Rfid(CheckerInterface):
    def __init__(self, delegate=None) -> None:
        self.delegate = delegate
        self.reader = SimpleMFRC522()
        self.card_presence = False
        self.array_detect_state = []

    def process(self):
        id, text = self.reader.read_no_block()
        if id:
            rfid_data = {
                "id": id,
                "text": text.replace(" ", "")
            }
            self.array_detect_state = []
            if self.delegate:
                self.delegate.rfid_detected(rfid_data)
                if not self.card_presence:
                    self.delegate.rfid_placed(rfid_data)
            self.card_presence = True
        else:
            rfid_data = {}
            self.array_detect_state.append(None)
            if len(self.array_detect_state) >= 2:
                self.array_detect_state = []
                if self.delegate:
                    self.delegate.rfid_not_detected()
                    if self.card_presence:
                        self.delegate.rfid_removed()
                self.card_presence = False

    def write_no_block(self, text_to_write):
        id, text = self.reader.write(text_to_write)
        if self.delegate:
            if id:
                self.delegate.rfid_has_written(text)
            else:
                self.delegate.rfid_not_written()

    def process_checker(self):
            start_time = time.time()
            try:
                while time.time() - start_time < 10:
                    id, text = self.reader.read_no_block()
                    if id:
                        return True
                    time.sleep(0.1)
            except Exception as e:
                pass
            return False
from Rfid import Rfid
from RfidDelegate import RfidDelegate
import time

class MyDelegate(RfidDelegate):
    def __init__(self) -> None:
        super().__init__()
        self.rfid = None
        self.activities = [
            "belotte",
            "echecs",
            "scrabble"
        ]
        self.actual_activities = 0
        self.writing = False

    def set_rfid(self, rfid):
        self.rfid = rfid

    def rfid_placed(self, rfid_data):
        super().rfid_placed(rfid_data)
        print(f"Data: {rfid_data}")

    def rfid_detected(self, rfid_data):
        super().rfid_detected(rfid_data)
        if self.rfid:
            if len(self.activities) > self.actual_activities:
                self.writing = True
                self.rfid.write_no_block(self.activities[self.actual_activities])
            else:
                if self.writing:
                    self.writing = False
                    print("Finished Writing")
        else:
            print("No rfid object")

    def rfid_not_written(self):
        super().rfid_not_written()
        print("Attempting to write...")

    def rfid_has_written(self, text):
        super().rfid_has_written(text)
        print(f"Written '{text}' with success!")
        time.sleep(1)
        self.actual_activities += 1

    def rfid_removed(self):
        super().rfid_removed()
        if self.writing:
            self.writing = False
            print("Fail to write")



my_delegate = MyDelegate()
rfid = Rfid(my_delegate)
my_delegate.set_rfid(rfid)

try:
    while True:
        rfid.process()
except KeyboardInterrupt:
    pass
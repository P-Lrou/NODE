from Rfid import Rfid
from RfidDelegate import RfidDelegate
import RPi.GPIO as GPIO

class MyDelegate(RfidDelegate):
    def __init__(self) -> None:
        super().__init__()
        self.rfid = None
        self.activities = [
            "belotte",
            "echecs",
            "scrabble",
            "tarot"
        ]
        self.actual_activities = 0
        self.writing = False
        self.block = False

    def set_rfid(self, rfid):
        self.rfid = rfid

    def rfid_placed(self, rfid_data):
        super().rfid_placed(rfid_data)
        print(f"Data: {rfid_data}")

    def rfid_detected(self, rfid_data):
        super().rfid_detected(rfid_data)
        if self.rfid:
            if len(self.activities) > self.actual_activities:
                if not self.block:
                    self.writing = True
                    self.rfid.write_no_block(self.activities[self.actual_activities])
                else:
                    print("Please remove the card")
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
        self.block = True
        print(f"Written '{text}' with success!")
        self.actual_activities += 1

    def rfid_removed(self):
        super().rfid_removed()
        self.block = False
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
    GPIO.cleanup()

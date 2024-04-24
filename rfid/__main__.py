from Rfid import Rfid
from RfidDelegate import RfidDelegate

class MyDelegate(RfidDelegate):
    def __init__(self) -> None:
        super().__init__()

    def rfid_placed(self, rfid_data):
        super().rfid_placed(rfid_data)
        print(f"id: {rfid_data['id']}")

my_delegate = MyDelegate()
rfid = Rfid(my_delegate)

try:
    while True:
        rfid.process()
except KeyboardInterrupt:
    pass
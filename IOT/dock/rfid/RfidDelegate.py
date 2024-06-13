from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dock.rfid.Rfid import Rfid
    from dock.rfid.Badge import Badge

class RfidDelegate:
    def __init__(self) -> None:
        pass

    def rfid_placed(self, badge: "Badge", rfid: "Rfid"):
        pass

    def rfid_removed(self, rfid: "Rfid"):
        pass

    def rfid_detected(self, badge: "Badge", rfid: "Rfid"):
        pass

    def rfid_not_detected(self, rfid: "Rfid"):
        pass
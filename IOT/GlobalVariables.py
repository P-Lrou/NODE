from tools.DLog import DLog

class LedPins:
    _instance = None

    def __init__(self):
        self.trafic_number: list[int] = []
        self.good_rfid_number: list[int] = []
        self.error_rfid_number: list[int] = []
        
        rfid_ids = RfidPins.instance().rfid_number
        if len(self.good_rfid_number) == len(rfid_ids):
            self.good_rfid_led_number: dict[str, int] = {str(id): self.good_rfid_number[key] for key, id in enumerate(rfid_ids)}
        else:
            DLog.LogError("No length matching between good_rfid_number and rfid_ids")

        if len(self.error_rfid_number) == len(rfid_ids):
            self.error_rfid_led_number: dict[str, int] = {str(id): self.error_rfid_number[key] for key, id in enumerate(rfid_ids)}
        else:
            DLog.LogError("No length matching between error_rfid_number and rfid_ids")

    @classmethod
    def instance(cls) -> "LedPins":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
class RfidPins:
    _instance = None

    def __init__(self) -> None:
        self.rfid_number = [2, 3, 4]

    @classmethod
    def instance(cls) -> "RfidPins":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


class Activities:
    _instance = None

    def __init__(self):
        self.activities = [
            "belotte",
            "echecs",
            "scrabble",
            "tarot",
            "bridge",
            "balade"
        ]

    @classmethod
    def instance(cls) -> "Activities":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
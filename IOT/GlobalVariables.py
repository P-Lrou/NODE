from tools.DLog import DLog
import time

class LedPins:
    _instance = None

    def __init__(self):
        self.trafic_number: list[int] = [14]
        self.good_rfid_number: list[int] = [23, 7, 20]
        self.error_rfid_number: list[int] = [24, 1, 21]
        
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
    
class NeoLedPins:
    _instance = None

    def __init__(self):
<<<<<<< Updated upstream
        self.pin_number: list[int] = [10, 12, 18]

    @classmethod
    def instance(cls) -> "NeoLedPins":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
class RfidPins:
    _instance = None

=======
        self.pin_number: int = 21
        self.nums_pixels: list[int] = [24, 24, 24]
        self.total_pixels: int = 72
        
          
class ButtonPins(Singleton):
>>>>>>> Stashed changes
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
            "belote",
            "triomino",
            "scrabble",
            "gouter",
            "petanque",
            "promenade"
        ]

    @classmethod
    def instance(cls) -> "Activities":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
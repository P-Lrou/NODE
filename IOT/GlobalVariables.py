from tools.DLog import DLog
import time

class Singleton:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

class LedPins(Singleton):
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
    
class NeoLedPins(Singleton):
    def __init__(self):
        self.pin_number: int = 21
        self.nums_pixels: list[int] = [24, 24, 24]
        self.total_pixels: int = 72
    
class RfidPins(Singleton):
  def __init__(self) -> None:
    self.rfid_number = [2, 3, 4]

          
class ButtonPins(Singleton):
    def __init__(self) -> None:
        self.sending_button_number = 16

        
class Activities(Singleton):
    def __init__(self):
        self.activities = [
            "belote",
            "triomino",
            "scrabble",
            "gouter",
            "petanque",
            "promenade"
        ]

class Path(Singleton):
    def __init__(self) -> None:
        self.init_sound = "ressources/sound/"
        self.rfid_sounds = [
            "Marimba1.wav",
            "Marimba2.wav",
            "Marimba3.wav",
        ]
        self.found_sound = "match_found.wav"
        self.error_sound = "error.wav"
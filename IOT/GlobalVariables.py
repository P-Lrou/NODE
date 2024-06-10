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
        self.trafic_number: list[int] = [17, 27, 22]
    
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

        self.init_image = "ressources/images/"
        self.init_font = "ressources/fonts/"
        self.fonts = {
            "arial_black": "ARIBLK.TTF"
        }

    def get_font_path(self, font_name):
        if font_name in self.fonts:
            return self.init_font + self.fonts[font_name]
        else:
            return ""
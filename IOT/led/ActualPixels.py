import board
import neopixel
class ActualPixels:
    _instance = None

    def __init__(self, pin_number: int = 21, total_pixels: int = 72) -> None:
        self.good_pins_number = [10, 12, 18, 21]
        self.pixel_pin = self._check_good_pin_number(pin_number)
        self.ORDER = neopixel.GRB
        self.pixels = neopixel.NeoPixel(
            self.pixel_pin, total_pixels, brightness=0.2, auto_write=False, pixel_order=self.ORDER
        )

    def _check_good_pin_number(self, pin_number: int):
        if pin_number not in self.good_pins_number:
            pin_number = self.good_pins_number[0]
        return getattr(board, f"D{pin_number}")

    @classmethod
    def instance(cls, pin_number: int = 21, total_pixels: int = 72) -> "ActualPixels":
        if cls._instance is None:
            cls._instance = cls(pin_number, total_pixels)
        return cls._instance
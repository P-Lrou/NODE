import board
import neopixel
from led.NeoLedStrategy import *

class NeoLed:
    def __init__(self, pin_number: int, num_pixels: int = 1, starting_pixel: int = 0, total_pixels: int = 72) -> None:
        self.good_pins_number: list[int] = [10, 12, 18, 21]
        self.pixel_pin = self._check_good_pin_number(pin_number)
        self.num_pixels = num_pixels
        self.starting_pixel = starting_pixel
        self.ORDER = neopixel.GRB
        ActualPixels.instance().pixels[str(self.pixel_pin)] = [(0, 0, 0) for _ in range(total_pixels)]
        self.pixels = neopixel.NeoPixel(
            self.pixel_pin, total_pixels, brightness=0.2, auto_write=False, pixel_order=self.ORDER
        )
        self.strategy = NoneStrategy(self)

    def _check_good_pin_number(self, pin_number: int):
        if pin_number not in self.good_pins_number:
            pin_number = self.good_pins_number[0]
        return getattr(board, f"D{pin_number}")

    def set_strategy(self, strategy):
        self.strategy = strategy

    def execute(self):
        self.strategy.execute()

    def circle(self, color, wait=0.1):
        self.set_strategy(CircleStrategy(self, color, wait))
    
    def pulse(self, color, wait=0.1):
        self.set_strategy(PulseStrategy(self, color, wait))

    def fill(self, color, brightness=1):
        self.set_strategy(FillStrategy(self, color, brightness))

    def _get_actual_pixels(self):
        for i in range(len(ActualPixels.instance().pixels[str(self.pixel_pin)])):
            self.pixels[i] = ActualPixels.instance().pixels[str(self.pixel_pin)][i]

    def _set_all_pixels(self, color, brightness=1):
        r, g, b = color
        self._get_actual_pixels()
        for i in range(self.num_pixels):
            self.pixels[i + self.starting_pixel] = (int(r * brightness), int(g * brightness), int(b * brightness))
            ActualPixels.instance().pixels[str(self.pixel_pin)][i + self.starting_pixel] = (int(r * brightness), int(g * brightness), int(b * brightness))
        self.pixels.show()

    def stop(self):
         self.set_strategy(NoneStrategy(self))

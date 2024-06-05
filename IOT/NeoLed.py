import time
import board
import neopixel
from RGB import RGB
"""
NeoLed is the class for the led ruban, so if we want to interact with the led ruban, we can use that
i also use a external class RGB to just put informations in it
"""
class NeoLed:
    def __init__(self, pin_number: int, num_pixels: int) -> None:
        self.pixel_pin = getattr(board, f"D{pin_number}")
        self.num_pixels = num_pixels
        # Actually order is GRB, probably should be RGB in the future no ? idk
        # but it actually works pretty well like that
        self.ORDER = neopixel.GRB
        self.pixels = neopixel.NeoPixel(
            self.pixel_pin, self.num_pixels, brightness=0.2, auto_write=False, pixel_order=self.ORDER
        )
        self.actualBrightness = 100
        self.currentColor = RGB(0, 0, 0)

    def process(self):
        color = self.currentColor
        brightness = self.actualBrightness
        self._set_all_pixels(RGB(color.red * brightness // 255, color.green * brightness // 255, color.blue * brightness // 255))
        
    def fill(self, color, brightness=1):
        self.stop()
        self._set_all_pixels(color, brightness)

    def _set_all_pixels(self, color: RGB, brightness=1):
        self.pixels.fill((int(color.red * brightness), int(color.green * brightness), int(color.blue * brightness)))
        self.pixels.show()

    def stop(self):
        self._set_all_pixels(RGB(0, 0, 0))

if __name__ == "__main__":
    # Example of use
    neoLed = NeoLed(pin_number=18, num_pixels=45)
    try:
        neoLed.pulse(RGB(0, 0, 255))  # Starts the pulsation effect in blue
        time.sleep(5)  # Wait 5 seconds before moving on to the next effect
    finally:
        neoLed.stop()  # Stop the effects
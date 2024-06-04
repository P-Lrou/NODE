# import time
# import board
# import neopixel
# import threading

# class NeoLed:
#     def __init__(self, pin_number: int, num_pixels: int) -> None:
#         self.good_pins_number: list[int] = [10, 12, 18, 21]
#         self.pixel_pin = self._check_good_pin_number(pin_number)
#         self.num_pixels = num_pixels
#         self.ORDER = neopixel.GRB
#         self.pixels = neopixel.NeoPixel(
#             self.pixel_pin, self.num_pixels, brightness=0.2, auto_write=False, pixel_order=self.ORDER
#         )
#         self.running = False
#         self.current_thread = None

#     def _check_good_pin_number(self, pin_number: int):
#         if pin_number not in self.good_pins_number:
#             pin_number = self.good_pins_number[0]
#         return getattr(board, f"D{pin_number}")

#     def _start_thread(self, target, args=()):
#         if self.running:
#             self.stop()
#             time.sleep(0.1)  # Small delay to ensure that the previous thread is stopped
#         self.running = True
#         self.current_thread = threading.Thread(target=target, args=args)
#         self.current_thread.start()

#     def circle(self, color, wait=0.1):
#         self._start_thread(self._run_circle, (color, wait))

#     def _run_circle(self, color, wait):
#         brightness_levels = [i / self.num_pixels for i in range(self.num_pixels)]
#         while self.running:
#             for j in range(self.num_pixels):
#                 r, g, b = color
#                 for i in range(self.num_pixels):
#                     brightness = brightness_levels[(i + j) % self.num_pixels]
#                     self.pixels[i] = (int(r * brightness), int(g * brightness), int(b * brightness))
#                 self.pixels.show()
#                 time.sleep(wait)
#             time.sleep(wait)

#     def pulse(self, color, wait=0.01):
#         self._start_thread(self._run_pulse, (color, wait))

#     def _run_pulse(self, color, wait):
#         r, g, b = color
#         while self.running:
#             for brightness in range(0, 256, 5):  # increasing brightness
#                 self._set_all_pixels((r * brightness // 255, g * brightness // 255, b * brightness // 255))
#                 time.sleep(wait)
#             for brightness in range(255, -1, -5):  # decreasing brightness
#                 self._set_all_pixels((r * brightness // 255, g * brightness // 255, b * brightness // 255))
#                 time.sleep(wait)
        
#     def fill(self, color, brightness=1):
#         self.stop()
#         self._set_all_pixels(color, brightness)

#     def _set_all_pixels(self, color, brightness=1):
#         r, g, b = color
#         self.pixels.fill((int(r * brightness), int(g * brightness), int(b * brightness)))
#         self.pixels.show()

#     def stop(self):
#         self.running = False
#         if self.current_thread is not None:
#             self.current_thread.join()  # Wait for the current thread to end
#         self._set_all_pixels((0, 0, 0))

# if __name__ == "__main__":
#     # Example of use
#     ring_led = NeoLed(pin_number=18, num_pixels=24)
#     try:
#         # ring_led.pulse((0, 0, 255))  # Starts the pulsation effect in blue
#         # time.sleep(5)  # Wait 5 seconds before moving on to the next effect
#         # ring_led.circle((0, 255, 0), wait=0.05)  # Starts the circle effect
#         # time.sleep(5)
#         ring_led.fill((255, 0, 0))
#         pass
#     finally:
#         ring_led.stop()  # Stop the effects
#         pass

# import time
# import board
# import neopixel

# class NeoLed:
#     def __init__(self, pin_number: int, num_pixels: int) -> None:
#         self.good_pins_number: list[int] = [10, 12, 18, 21]
#         self.pixel_pin = self._check_good_pin_number(pin_number)
#         self.num_pixels = num_pixels
#         self.ORDER = neopixel.GRB
#         self.pixels = neopixel.NeoPixel(
#             self.pixel_pin, self.num_pixels, brightness=0.2, auto_write=False, pixel_order=self.ORDER
#         )

#     def _check_good_pin_number(self, pin_number: int):
#         if (pin_number not in self.good_pins_number):
#             pin_number = self.good_pins_number[0]
#         return getattr(board, f"D{pin_number}")

#     def circle(self, color, wait=0.1, cycles=1):
#         brightness_levels = [i / self.num_pixels for i in range(self.num_pixels)]
#         for _ in range(cycles):
#             for j in range(self.num_pixels):
#                 r, g, b = color
#                 for i in range(self.num_pixels):
#                     brightness = brightness_levels[(i + j) % self.num_pixels]
#                     self.pixels[i] = (int(r * brightness), int(g * brightness), int(b * brightness))
#                 self.pixels.show()
#                 time.sleep(wait)
#             time.sleep(wait)

#     def pulse(self, color, wait=0.01, cycles=1):
#         r, g, b = color
#         for _ in range(cycles):
#             for brightness in range(0, 256, 5):  # increasing brightness
#                 self._set_all_pixels((r * brightness // 255, g * brightness // 255, b * brightness // 255))
#                 time.sleep(wait)
#             for brightness in range(255, -1, -5):  # decreasing brightness
#                 self._set_all_pixels((r * brightness // 255, g * brightness // 255, b * brightness // 255))
#                 time.sleep(wait)

#     def fill(self, color, brightness=1):
#         self._set_all_pixels(color, brightness)

#     def _set_all_pixels(self, color, brightness=1):
#         r, g, b = color
#         self.pixels.fill((int(r * brightness), int(g * brightness), int(b * brightness)))
#         self.pixels.show()

#     def stop(self):
#         self._set_all_pixels((0, 0, 0))

# if __name__ == "__main__":
#     # Example of use
#     ring_led = NeoLed(pin_number=18, num_pixels=24)
#     try:
#         ring_led.pulse((0, 0, 255), cycles=5)  # Pulsation effect in blue for 5 cycles
#         ring_led.circle((0, 255, 0), wait=0.05, cycles=5)  # Circle effect in green for 5 cycles
#         ring_led.fill((255, 0, 0))  # Fill the LEDs with red
#     finally:
#         ring_led.stop()  # Stop the effects

import board
import neopixel
from led.NeoLedStrategy import *

class NeoLed:
    def __init__(self, pin_number: int, num_pixels: int) -> None:
        self.good_pins_number: list[int] = [10, 12, 18, 21]
        self.pixel_pin = self._check_good_pin_number(pin_number)
        self.num_pixels = num_pixels
        self.ORDER = neopixel.GRB
        self.pixels = neopixel.NeoPixel(
            self.pixel_pin, self.num_pixels, brightness=0.2, auto_write=False, pixel_order=self.ORDER
        )
        self.strategy = NoneStrategy(self)

    def _check_good_pin_number(self, pin_number: int):
        if pin_number not in self.good_pins_number and False:
            pin_number = self.good_pins_number[0]
        return getattr(board, f"D{pin_number}")

    def set_strategy(self, strategy):
        print(self.pixel_pin)
        self.strategy = strategy

    def execute(self):
        self.strategy.execute()

    def circle(self, color, wait=0.1):
        self.set_strategy(CircleStrategy(self, color, wait))
    
    def pulse(self, color, wait=0.01):
        self.set_strategy(PulseStrategy(self, color, wait))

    def fill(self, color, brightness=1):
        self.set_strategy(FillStrategy(self, color, brightness))

    def _set_all_pixels(self, color, brightness=1):
        r, g, b = color
        self.pixels.fill((int(r * brightness), int(g * brightness), int(b * brightness)))
        self.pixels.show()

    def stop(self):
         self.set_strategy(NoneStrategy(self))
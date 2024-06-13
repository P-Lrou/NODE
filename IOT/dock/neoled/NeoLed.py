import time
import threading
from dock.neoled.ActualPixels import ActualPixels
from tools.DLog import DLog

class NeoLed:
    def __init__(self, pin_number: int, num_pixels: int = 1, starting_pixel: int = 0, total_pixels: int = 72) -> None:
        self.num_pixels = num_pixels
        self.starting_pixel = starting_pixel
        self.stop_event = threading.Event()
        self.current_thread = None
        ActualPixels.instance(pin_number, total_pixels)

    def _start_thread(self, target, args=()):
        if self.current_thread is not None and self.current_thread.is_alive():
            self.stop_event.set()
            self.current_thread.join()
        self.stop_event.clear()
        self.current_thread = threading.Thread(target=target, args=args)
        self.current_thread.start()

    def circle(self, color, wait=0.1):
        self._start_thread(self._run_circle, (color, wait))

    def _run_circle(self, color, wait):
        brightness_levels = [i / self.num_pixels for i in range(self.num_pixels)]
        try:
            while not self.stop_event.is_set():
                for j in range(self.num_pixels):
                    r, g, b = color
                    for i in range(self.num_pixels):
                        brightness = brightness_levels[(i + j) % self.num_pixels]
                        ActualPixels.instance().pixels[i + self.starting_pixel] = (int(r * brightness), int(g * brightness), int(b * brightness))
                    ActualPixels.instance().pixels.show()
                    time.sleep(wait)
                    if self.stop_event.is_set():
                        break
                time.sleep(wait)
        except KeyboardInterrupt:
            DLog.Log("Stop circle")

    def pulse(self, color, wait=0.01):
        self._start_thread(self._run_pulse, (color, wait))

    def _run_pulse(self, color, wait):
        r, g, b = color
        try:
            while not self.stop_event.is_set():
                for brightness in range(0, 256, 5):  # increasing brightness
                    self._set_all_pixels((r * brightness // 255, g * brightness // 255, b * brightness // 255))
                    time.sleep(wait)
                    if self.stop_event.is_set():
                        break
                for brightness in range(255, -1, -5):  # decreasing brightness
                    self._set_all_pixels((r * brightness // 255, g * brightness // 255, b * brightness // 255))
                    time.sleep(wait)
                    if self.stop_event.is_set():
                        break
        except KeyboardInterrupt:
            DLog.Log("Stop pulse")
        
    def fill(self, color, brightness=1):
        self.stop()
        self._set_all_pixels(color, brightness)

    def _set_all_pixels(self, color, brightness=1):
        r, g, b = color
        for i in range(self.num_pixels):
            ActualPixels.instance().pixels[i + self.starting_pixel] = (int(r * brightness), int(g * brightness), int(b * brightness))
        ActualPixels.instance().pixels.show()

    def stop(self):
        self.stop_event.set()
        if self.current_thread is not None:
            self.current_thread.join()
        self._set_all_pixels((0, 0, 0))

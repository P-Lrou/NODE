import time
import board
import neopixel
import threading

class RingLed:
    def __init__(self) -> None:
        self.pixel_pin = board.D18
        self.num_pixels = 24
        self.ORDER = neopixel.GRB
        self.pixels = neopixel.NeoPixel(
            self.pixel_pin, self.num_pixels, brightness=0.2, auto_write=False, pixel_order=self.ORDER
        )
        self.running = False
        self.current_thread = None

    def _start_thread(self, target, args=()):
        if self.running:
            self.stop()
            time.sleep(0.1)  # Petit délai pour s'assurer que le thread précédent est arrêté
        self.running = True
        self.current_thread = threading.Thread(target=target, args=args)
        self.current_thread.start()

    def circle(self, color, wait=0.1):
        self._start_thread(self._run_circle, (color, wait))

    def _run_circle(self, color, wait):
        brightness_levels = [i / self.num_pixels for i in range(self.num_pixels)]
        while self.running:
            for j in range(self.num_pixels):
                r, g, b = color
                for i in range(self.num_pixels):
                    brightness = brightness_levels[(i + j) % self.num_pixels]
                    self.pixels[i] = (int(r * brightness), int(g * brightness), int(b * brightness))
                self.pixels.show()
                time.sleep(wait)
            time.sleep(wait)

    def pulse(self, color, wait=0.01):
        self._start_thread(self._run_pulse, (color, wait))

    def _run_pulse(self, color, wait):
        r, g, b = color
        while self.running:
            for brightness in range(0, 256, 5):  # increasing brightness
                self._set_all_pixels((r * brightness // 255, g * brightness // 255, b * brightness // 255))
                time.sleep(wait)
            for brightness in range(255, -1, -5):  # decreasing brightness
                self._set_all_pixels((r * brightness // 255, g * brightness // 255, b * brightness // 255))
                time.sleep(wait)
        
    def fill(self, color):
        self.stop()
        self._set_all_pixels(color)

    def _set_all_pixels(self, color):
        self.pixels.fill(color)
        self.pixels.show()

    def stop(self):
        self.running = False
        if self.current_thread is not None:
            self.current_thread.join()  # Attendre que le thread actuel se termine
        self._set_all_pixels((0, 0, 0))

if __name__ == "__main__":
    # Exemple d'utilisation
    ring_led = RingLed()
    try:
        # ring_led.pulse((0, 0, 255))  # Lance l'effet de pulsation en bleu
        # time.sleep(5)  # Attendre 5 secondes avant de passer à l'effet suivant
        ring_led.circle((0, 255, 0), wait=0.05)  # Lance l'effet cercle
        # time.sleep(5)
        time.sleep(60)
    finally:
        ring_led.stop()  # Arrêter les effets


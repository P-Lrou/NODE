import time

class Strategy:
    def __init__(self, neo_led):
        self.neo_led = neo_led

    def execute(self):
        pass

class CircleStrategy(Strategy):
    def __init__(self, neo_led, color, wait):
        super().__init__(neo_led)
        self.color = color
        self.wait = wait
        self.step = 0

    def execute(self):
        brightness_levels = [i / self.neo_led.num_pixels for i in range(self.neo_led.num_pixels)]
        r, g, b = self.color
        for i in range(self.neo_led.num_pixels):
            brightness = brightness_levels[(i + self.step) % self.neo_led.num_pixels]
            self.neo_led.pixels[i + self.neo_led.starting_pixel] = (int(r * brightness), int(g * brightness), int(b * brightness))
        self.neo_led.pixels.show()
        self.step = (self.step + 1) % self.neo_led.num_pixels
        time.sleep(self.wait)

class PulseStrategy(Strategy):
    def __init__(self, neo_led, color, wait):
        super().__init__(neo_led)
        self.color = color
        self.wait = wait
        self.step = 0
        self.direction = 1

    def execute(self):
        r, g, b = self.color
        brightness = self.step / 255
        self.neo_led._set_all_pixels((int(r * brightness), int(g * brightness), int(b * brightness)))
        self.step += self.direction * 5
        if self.step >= 255 or self.step <= 0:
            self.direction *= -1
        time.sleep(self.wait)

class FillStrategy(Strategy):
    def __init__(self, neo_led, color, brightness):
        super().__init__(neo_led)
        self.color = color
        self.brightness = brightness

    def execute(self):
        self.neo_led._set_all_pixels(self.color, self.brightness)

class NoneStrategy(Strategy):
    def execute(self):
        self.neo_led._set_all_pixels((0, 0, 0))
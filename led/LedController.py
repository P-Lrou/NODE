from Led import Led
import time

class LedDictionnary:
    led_pins = {
        17: "rouge",
        27: "rouge",
        22: "rouge",
        6 : "vert",
        13: "vert",
        19: "vert",
        26: "vert"
    }

class LEDController:
    def __init__(self, pin_numbers):

        self.leds = []
        for pin_number in pin_numbers:
            self.leds.append(Led(pin_number))
        self.counter = 0

    def test_all(self):
        for led in self.leds:
            led.on()
            time.sleep(0.7)
        for led in self.leds:
            led.off()
            time.sleep(0.7)

    def on(self):
        led = self.leds[self.counter]
        led.on()
        if self.counter < len(self.leds)-1:
            self.counter += 1

    def off(self):
        led = self.leds[self.counter]
        led.off()
        if self.counter > 0:
            self.counter -= 1

    def toggle(self):
        for led in self.leds:
            led.toggle

    def all_on(self):
        for led in self.leds:
            led.on()

    def all_off(self):
        for led in self.leds:
            led.off()

    def close(self):
        for led in self.leds:
            led.close()
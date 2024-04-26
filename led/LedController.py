from multipledispatch import dispatch
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
        self.leds_by_pin = {}
        for pin_number in pin_numbers:
            led = Led(pin_number)
            self.leds.append(led)
            self.leds_by_pin[pin_number] = led
        self.counter = 0

    def test_all(self):
        for led in self.leds:
            led.on()
            time.sleep(0.7)
        for led in self.leds:
            led.off()
            time.sleep(0.7)

    @dispatch()
    def on(self):
        led = self.leds[self.counter]
        led.on()
        if self.counter < len(self.leds)-1:
            self.counter += 1
    
    @dispatch(int)
    def on(self, pin_number):
        if pin_number in self.leds_by_pin:
            led = self.leds_by_pin[pin_number]
            led.on()
        else:
            print("This pin number has not been instantiated")

    @dispatch()
    def off(self):
        led = self.leds[self.counter]
        led.off()
        if self.counter > 0:
            self.counter -= 1

    @dispatch(int)
    def off(self, pin_number):
        if pin_number in self.leds_by_pin:
            led = self.leds_by_pin[pin_number]
            led.off()
        else:
            print("This pin number has not been instantiated")

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
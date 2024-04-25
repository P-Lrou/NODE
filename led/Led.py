import RPi.GPIO as GPIO
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
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

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

class Led:
    def __init__(self, pin_number) -> None:
        self.pin_number = pin_number
        GPIO.setup(self.pin_number, GPIO.OUT)
        GPIO.output(self.pin_number, GPIO.LOW)
        self.state = GPIO.LOW
    
    def on(self):
        GPIO.output(self.pin_number, GPIO.HIGH)
        self.state = GPIO.HIGH
    
    def off(self):
        GPIO.output(self.pin_number, GPIO.LOW)
        self.state = GPIO.LOW

    def toggle(self):
        GPIO.output(self.pin_number, not self.state)


if __name__ == "__main__":
    led_controller = LEDController(LedDictionnary.led_pins.keys())
    led_controller.all_off()

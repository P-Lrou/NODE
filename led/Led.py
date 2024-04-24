import RPi.GPIO as GPIO
import time

class LEDController:
    def __init__(self, pin_numbers):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.leds = pin_numbers
        for pin in self.leds:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

    def on(self, led_index):
        if 0 <= led_index < len(self.leds):
            GPIO.output(self.leds[led_index], GPIO.HIGH)

    def off(self, led_index):
        if 0 <= led_index < len(self.leds):
            GPIO.output(self.leds[led_index], GPIO.LOW)

    def toggle(self, led_index):
        if 0 <= led_index < len(self.leds):
            current_value = GPIO.input(self.leds[led_index])
            GPIO.output(self.leds[led_index], not current_value)

    def all_on(self):
        for led in self.leds:
            GPIO.output(led, GPIO.HIGH)

    def all_off(self):
        for led in self.leds:
            GPIO.output(led, GPIO.LOW)

if __name__ == "__main__":
    led_pins = [23, 27, 22]
    led_controller = LEDController(led_pins)
    led_controller.all_on()
    time.sleep(1)
    led_controller.all_off()

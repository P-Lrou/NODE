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

#* MAKE SURE TO CLOSE AT THE END OF YOUR CODE
class LEDController:
    def __del__(self):
        self.close()
        
    def __init__(self, pin_numbers=None, pin_by_name=None):
        self.counter = 0
        self.leds = []
        self.leds_by_pin = {}
        self.key_type = None
        if pin_numbers is None and pin_by_name is None:
            print("Error: pin_numbers and pin_by_name is None")
        elif pin_number is not None and pin_by_name is not None:
            print("Error: You can not instanciate leds by pin_numbers and pin_by_name")
        else:
            if pin_numbers is not None:
                if isinstance(pin_numbers, list):
                    self.key_type = int
                    if pin_numbers:
                        for pin_number in pin_numbers:
                            led = Led(pin_number)
                            self.leds.append(led)
                            self.leds_by_pin[pin_number] = led
                    else:
                        print("Error: pin_numbers is empty")
                else:
                    print("Error: pin_number is not a list")
            elif pin_by_name is not None:
                if isinstance(pin_by_name, dict):
                    self.key_type = str
                    if pin_by_name:
                        for name in pin_by_name:
                            led = Led(pin_by_name[name])
                            self.leds.append(led)
                            self.leds_by_pin = pin_by_name
                    else:
                        print("Error: pin_by_name is empty")
                else:
                    print("Error: pin_by_name is not a dictionnary")

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
        if self.key_type == int:
            if pin_number in self.leds_by_pin:
                led = self.leds_by_pin[pin_number]
                led.on()
            else:
                print("This pin number has not been instantiated")
        else:
            print("Error: leds have been instanciated by int keys")
    
    @dispatch(str)
    def on(self, pin_name):
        if self.key_type == str:
            if pin_name in self.leds_by_pin:
                led = self.leds_by_pin[pin_name]
                led.on()
            else:
                print("This pin name has not been instantiated")
        else:
            print("Error: leds have been instanciated by string keys")

    @dispatch()
    def off(self):
        led = self.leds[self.counter]
        led.off()
        if self.counter > 0:
            self.counter -= 1

    @dispatch(int)
    def off(self, pin_number):
        if self.key_type == int:
            if pin_number in self.leds_by_pin:
                led = self.leds_by_pin[pin_number]
                led.off()
            else:
                print("This pin number has not been instantiated")
        else:
            print("Error: leds have been instanciated by int keys")
    
    @dispatch(str)
    def off(self, pin_name):
        if self.key_type == str:
            if pin_name in self.leds_by_pin:
                led = self.leds_by_pin[pin_name]
                led.off()
            else:
                print("This pin name has not been instantiated")
        else:
            print("Error: leds have been instanciated by string keys")

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
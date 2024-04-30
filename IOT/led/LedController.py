from led.Led import Led
from tools.DLog import DLog
import time

#* MAKE SURE TO CLOSE AT THE END OF YOUR CODE
class LEDController:
        
    def __init__(self, pin_numbers=None, pin_by_name=None):
        self.counter = 0
        self.leds = []
        self.leds_by_pin = {}
        self.key_type = None
        if pin_numbers is None and pin_by_name is None:
            DLog.LogError("pin_numbers and pin_by_name is None")
        elif pin_numbers is not None and pin_by_name is not None:
            DLog.LogError("You can not instanciate leds by pin_numbers and pin_by_name")
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
                        DLog.LogError("pin_numbers is empty")
                else:
                    DLog.LogError("pin_numbers is not a list")
            elif pin_by_name is not None:
                if isinstance(pin_by_name, dict):
                    self.key_type = str
                    if pin_by_name:
                        for name in pin_by_name:
                            led = Led(pin_by_name[name])
                            self.leds.append(led)
                            self.leds_by_pin[name] = led
                    else:
                        DLog.LogError("pin_by_name is empty")
                else:
                    DLog.LogError("pin_by_name is not a dictionnary")

    def test_all(self):
        for led in self.leds:
            led.on()
            time.sleep(0.7)
        for led in self.leds:
            led.off()
            time.sleep(0.7)

    def on_next(self):
        led = self.leds[self.counter]
        led.on()
        if self.counter < len(self.leds)-1:
            self.counter += 1
    
    def on_int(self, pin_number):
        if self.key_type == int:
            if pin_number in self.leds_by_pin:
                led = self.leds_by_pin[pin_number]
                led.on()
            else:
                DLog.LogError("This pin number has not been instantiated")
        else:
            DLog.LogError("leds have been instanciated by int keys")
    
    def on_name(self, pin_name):
        if self.key_type == str:
            if pin_name in self.leds_by_pin:
                led = self.leds_by_pin[pin_name]
                led.on()
            else:
                DLog.LogError("This pin name has not been instantiated")
        else:
            DLog.LogError("leds have been instanciated by string keys")

    def off_previous(self):
        if self.counter > 0:
            self.counter -= 1
        led = self.leds[self.counter]
        led.off()

    def off_int(self, pin_number):
        if self.key_type == int:
            if pin_number in self.leds_by_pin:
                led = self.leds_by_pin[pin_number]
                led.off()
            else:
                DLog.LogError("This pin number has not been instantiated")
        else:
            DLog.LogError("leds have been instanciated by int keys")
    
    def off_name(self, pin_name):
        if self.key_type == str:
            if pin_name in self.leds_by_pin:
                led = self.leds_by_pin[pin_name]
                led.off()
            else:
                DLog.LogError("This pin name has not been instantiated")
        else:
            DLog.LogError("leds have been instanciated by string keys")

    def toggle(self):
        for led in self.leds:
            led.toggle

    def all_on(self):
        for led in self.leds:
            led.on()
        self.counter = len(self.leds)-1

    def all_off(self):
        for led in self.leds:
            led.off()
        self.counter = 0

    def blinking(self):
        for i in range(0, 5):
            for led in self.leds:
                led.off()
                time.sleep(0.3)
            for led in self.leds:
                led.on()
                time.sleep(0.3)
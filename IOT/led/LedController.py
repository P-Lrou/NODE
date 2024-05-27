from led.Led import Led
from tools.DLog import DLog
import time

#* MAKE SURE TO CLOSE AT THE END OF YOUR CODE
class LEDController:
        
    def __init__(self, pin_numbers: list[int] = None, pin_by_name: dict[str, int]=None):
        self.counter = 0
        self.leds: list[Led] = []
        self.leds_by_pin: dict[any, Led] = {}
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
                            if pin_number != 0:
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
                        for name, pin_number in pin_by_name.items():
                            if pin_number != 0:
                                led = Led(pin_number)
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
    
    def on_int(self, pin_number: int) -> bool:
        if self.key_type == int:
            if pin_number in self.leds_by_pin:
                led = self.leds_by_pin[pin_number]
                led.on()
                return True
            else:
                DLog.LogError("This pin number has not been instantiated")
        else:
            DLog.LogError("leds have been instanciated by int keys")
        return False
    
    def on_name(self, pin_name: str) -> bool:
        if self.key_type == str:
            if pin_name in self.leds_by_pin:
                led = self.leds_by_pin[pin_name]
                led.on()
                return True
            else:
                DLog.LogError("This pin name has not been instantiated")
        else:
            DLog.LogError("leds have been instanciated by string keys")
        return False

    def off_previous(self):
        if self.counter > 0:
            self.counter -= 1
        led = self.leds[self.counter]
        led.off()

    def off_int(self, pin_number: int) -> bool:
        if self.key_type == int:
            if pin_number in self.leds_by_pin:
                led = self.leds_by_pin[pin_number]
                led.off()
                return True
            else:
                DLog.LogError("This pin number has not been instantiated")
        else:
            DLog.LogError("leds have been instanciated by int keys")
        return False
    
    def off_name(self, pin_name: str) -> bool:
        if self.key_type == str:
            if pin_name in self.leds_by_pin:
                led = self.leds_by_pin[pin_name]
                led.off()
                return True
            else:
                DLog.LogError("This pin name has not been instantiated")
        else:
            DLog.LogError("leds have been instanciated by string keys")
        return False

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

    def blink_int(self, pin_number: str, blinking_repeat: int = 5) -> bool:
        for i in range (0, blinking_repeat):
            if not self.on_int(pin_number):
                return False
            time.sleep(0.3)
            if not self.off_int(pin_number):
                return False
        return True
    
    def blink_name(self, pin_name: str, blinking_repeat: int = 5, delta_time_seconds: int = 0.3) -> bool:
        for i in range (0, blinking_repeat):
            if not self.on_name(pin_name):
                return False
            time.sleep(delta_time_seconds)
            if not self.off_name(pin_name):
                return False
        return True

    def all_blinking(self, blinking_repeat: int = 5, delta_time_seconds: int = 0.3):
        for i in range(0, blinking_repeat):
            for led in self.leds:
                led.on()
            time.sleep(delta_time_seconds)
            for led in self.leds:
                led.off()
            time.sleep(delta_time_seconds)

    def blinking(self, blinking_repeat: int = 5, delta_time_seconds: int = 0.3):
        for i in range(0, blinking_repeat):
            for led in self.leds:
                led.off()
                time.sleep(delta_time_seconds)
            for led in self.leds:
                led.on()
                time.sleep(delta_time_seconds)
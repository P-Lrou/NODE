from LedController import *

led_controller = LEDController(LedDictionnary.led_pins.keys())
led_controller.all_off()
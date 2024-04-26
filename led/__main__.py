from LedController import *
import time
led_controller = LEDController(LedDictionnary.led_pins.keys())
led_controller.on()
led_controller.on(3)

time.sleep(5)
led_controller.close()
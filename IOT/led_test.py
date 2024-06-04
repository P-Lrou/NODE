from led.NeoLed import NeoLed
from led.NeoLedStrategy import *
import time

ring_led = NeoLed(pin_number=18, num_pixels=24)
effect = True  # Boolean to switch between circle and pulse

try:
    switch_interval = 5  # Switch effect every 5 seconds
    next_switch_time = time.time() + switch_interval

    while True:
        current_time = time.time()
        if current_time >= next_switch_time:
            effect = not effect
            if effect:
                ring_led.circle((0, 255, 0))
            else:
                ring_led.pulse((0, 0, 255))
            next_switch_time = current_time + switch_interval

        ring_led.execute()

except KeyboardInterrupt:
    ring_led.stop()  # Ensure the LEDs are turned off when exiting
    ring_led.execute()

from led.NeoLed import NeoLed
from led.NeoLedStrategy import *
import time

# Configuration des anneaux LED
ring_led_1 = NeoLed(pin_number=21, num_pixels=24, starting_pixel=0, total_pixels=72)
ring_led_2 = NeoLed(pin_number=21, num_pixels=24, starting_pixel=24, total_pixels=72)
ring_led_3 = NeoLed(pin_number=21, num_pixels=24, starting_pixel=48, total_pixels=72)

# Fonction pour exécuter un effet LED en boucle
def run_led_effect(led, effect=True):
    switch_interval = 5  # Switch effect every 5 seconds
    next_switch_time = time.time() + switch_interval

    try:
        while True:
            current_time = time.time()
            if current_time >= next_switch_time:
                effect = not effect
                if effect:
                    led.circle((255, 0, 0), wait=0.1)
                else:
                    led.pulse((0, 0, 255), wait=0.01)
                next_switch_time = current_time + switch_interval

            led.execute()
            time.sleep(0.01)  # Add a small delay to prevent rapid flickering
    except KeyboardInterrupt:
        led.stop()  # Ensure the LEDs are turned off when exiting
        led.execute()

# Lancer les effets LED sur les anneaux séparés dans des threads différents
import threading

thread_1 = threading.Thread(target=run_led_effect, args=(ring_led_1,))
thread_2 = threading.Thread(target=run_led_effect, args=(ring_led_2,))
thread_3 = threading.Thread(target=run_led_effect, args=(ring_led_3,))

thread_1.start()
time.sleep(1)
thread_2.start()
time.sleep(1)
thread_3.start()

# Join threads to wait for their completion
thread_1.join()
thread_2.join()
thread_3.join()

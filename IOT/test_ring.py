import time
from led.NeoLed import NeoLed

def main():
    ring_led = NeoLed(pin_number=21, num_pixels=24, total_pixels=72, starting_pixel=24)
    effect = True  # Boolean to switch between circle and pulse

    try:
        switch_interval = 5  # Switch effect every 5 seconds
        next_switch_time = time.time() + switch_interval

        while True:
            current_time = time.time()
            if current_time >= next_switch_time:
                effect = not effect
                if effect:
                    ring_led.circle(color=(0, 255, 0), wait=0.1)
                else:
                    ring_led.pulse(color=(0, 0, 255), wait=0.01)
                next_switch_time = current_time + switch_interval

            ring_led.execute()

    except KeyboardInterrupt:
        ring_led.stop()  # Ensure the LEDs are turned off when exiting

if __name__ == "__main__":
    main()

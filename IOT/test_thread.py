import time
from led.NeoLed import NeoLed

def main():
    active1 = True
    active2 = True
    active3 = True
    ring_led1 = NeoLed(pin_number=21, num_pixels=24, total_pixels=72, starting_pixel=0)
    ring_led2 = NeoLed(pin_number=21, num_pixels=24, total_pixels=72, starting_pixel=24)
    ring_led3 = NeoLed(pin_number=21, num_pixels=24, total_pixels=72, starting_pixel=48)
    effect1 = True  # Boolean to switch between circle and pulse
    effect2 = True  # Boolean to switch between circle and pulse
    effect3 = True  # Boolean to switch between circle and pulse

    try:
        switch_interval1 = 3  # Switch effect every 5 seconds
        switch_interval2 = 5  # Switch effect every 5 seconds
        switch_interval3 = 7  # Switch effect every 5 seconds

        next_switch_time1 = time.time()
        next_switch_time2 = time.time()
        next_switch_time3 = time.time()

        while True:
            current_time = time.time()

            if active1:
                if current_time >= next_switch_time1:
                    effect1 = not effect1
                    if effect1:
                        ring_led1.circle(color=(0, 255, 0), wait=0.1)
                    else:
                        ring_led1.pulse(color=(0, 0, 255), wait=0.01)
                    next_switch_time1 = current_time + switch_interval1
            
            if active2:
                if current_time >= next_switch_time2:
                    effect2 = not effect2
                    if effect2:
                        ring_led2.circle(color=(0, 255, 0), wait=0.1)
                    else:
                        ring_led2.pulse(color=(0, 0, 255), wait=0.01)
                    next_switch_time2 = current_time + switch_interval2
            
            if active3:
                if current_time >= next_switch_time3:
                    effect3 = not effect3
                    if effect3:
                        ring_led3.circle(color=(0, 255, 0), wait=0.1)
                    else:
                        ring_led3.pulse(color=(0, 0, 255), wait=0.01)
                    next_switch_time3 = current_time + switch_interval3

    except KeyboardInterrupt:
        ring_led1.stop()  # Ensure the LEDs are turned off when exiting
        ring_led2.stop()  # Ensure the LEDs are turned off when exiting
        ring_led3.stop()  # Ensure the LEDs are turned off when exiting

if __name__ == "__main__":
    main()

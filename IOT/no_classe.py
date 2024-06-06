import board
import neopixel
import time

pixels_num = 24
total_pixels = 72
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(board.D21, total_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER)

step = 0
wait_on = 0.5
wait_off = 0.5
wait_circle = 0.02
wait_pulse = 0.01
direction = 1

def on(starting, color = (255, 0, 0)):
    global pixels, wait_on, pixels_num
    for i in range(pixels_num):
        pixels[i + starting] = color
    pixels.show()
    time.sleep(wait_on)

def off(starting):
    global pixels, wait_off, pixels_num
    for i in range(pixels_num):
        pixels[i + starting] = (0, 0, 0)
    pixels.show()
    time.sleep(wait_off)

def circle(starting, color = (255, 0, 0)):
    global step, pixels, wait_circle, pixels_num
    brightness_levels = [i / pixels_num for i in range(pixels_num)]
    # brightness_levels.reverse()
    r, g, b = color
    for i in range(pixels_num):
        brightness = brightness_levels[(i + step) % pixels_num]
        pixels[i + starting] = (int(r * brightness), int(g * brightness), int(b * brightness))
    pixels.show()
    step = (step + 1) % pixels_num
    time.sleep(wait_circle)

def pulse(starting, color = (255, 0, 0)):
    global step, pixels, wait_pulse, pixels_num, direction
    r, g, b = color
    brightness = step / 255
    for i in range(pixels_num):
        pixels[i + starting] = (int(r * brightness), int(g * brightness), int(b * brightness))
    pixels.show()
    step += direction * 5
    if step >= 255 or step <= 0:
        direction *= -1
    time.sleep(wait_pulse)


strategy = "on"
# strategy = "circle"
# strategy = "pulse"

try:
    while True:
        if strategy == "on":
            on(0, (0, 255, 0))
            on(24, (0, 0, 255))
            on(48, (255, 0, 0))
            off(0)
            off(24)
            off(48)
        elif strategy == "circle":
            circle(0)
            circle(24)
            circle(48)
        elif strategy == "pulse":
            pulse(0)
            pulse(24)
            pulse(48)
except KeyboardInterrupt:
    pass

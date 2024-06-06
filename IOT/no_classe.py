import board
import neopixel
import time

pixels_num = 24
total_pixels = 72
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(board.D21, total_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER)

step = 0
color = (255, 0, 0)
wait = 0.01
direction = 1

def circle(starting):
    global step, pixels, wait, pixels_num
    brightness_levels = [i / pixels_num for i in range(pixels_num)]
    # brightness_levels.reverse()
    r, g, b = color
    for i in range(pixels_num):
        brightness = brightness_levels[(i + step) % pixels_num]
        pixels[i + starting] = (int(r * brightness), int(g * brightness), int(b * brightness))
    pixels.show()
    step = (step + 1) % pixels_num
    time.sleep(wait)

def pulse(starting):
    global step, pixels, wait, pixels_num, direction
    r, g, b = color
    brightness = step / 255
    for i in range(pixels_num):
        pixels[i + starting] = (int(r * brightness), int(g * brightness), int(b * brightness))
    pixels.show()
    step += direction * 5
    if step >= 255 or step <= 0:
        direction *= -1
    time.sleep(wait)

try:
    while True:
        circle(0)
        circle(24)
        circle(48)
        # pulse(0)
        # pulse(24)
        # pulse(48)
except KeyboardInterrupt:
    pass

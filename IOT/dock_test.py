from dock.Dock import Dock
import time
import gc

# Fonction pour initialiser les docks
def init_docks():
    dock1 = Dock()
    dock1.set_ring_led(pin_number=21, num_pixels=24, starting_pixel=0, total_pixels=48)
    dock2 = Dock()
    dock2.set_ring_led(pin_number=21, num_pixels=24, starting_pixel=24, total_pixels=48)
    dock3 = Dock()
    dock3.set_ring_led(pin_number=18, num_pixels=24, starting_pixel=0, total_pixels=24)
    return dock1, dock2, dock3

# Fonction pour libérer les ressources des docks
def cleanup_docks(docks):
    for dock in docks:
        dock.launch_stop()
        dock.execute_led()
    gc.collect()  # Forcer le ramasse-miettes

dock1, dock2, dock3 = init_docks()

try:
    switch_interval_1 = 5
    switch_interval_2 = 7
    switch_interval_3 = 9

    next_switch_time_1 = time.time() + switch_interval_1
    next_switch_time_2 = time.time() + switch_interval_2
    next_switch_time_3 = time.time() + switch_interval_3

    effect_1 = True
    effect_2 = True
    effect_3 = True

    while True:
        current_time = time.time()

        if current_time >= next_switch_time_1:
            effect_1 = not effect_1
            if effect_1:
                dock1.launch_circle()
            else:
                dock1.launch_pulse()
            next_switch_time_1 = current_time + switch_interval_1

        if current_time >= next_switch_time_2:
            effect_2 = not effect_2
            if effect_2:
                dock2.launch_circle()
            else:
                dock2.launch_pulse()
            next_switch_time_2 = current_time + switch_interval_2

        if current_time >= next_switch_time_3:
            effect_3 = not effect_3
            if effect_3:
                dock3.launch_circle()
            else:
                dock3.launch_pulse()
            next_switch_time_3 = current_time + switch_interval_3

        dock1.execute_led()
        time.sleep(0.01)
        dock2.execute_led()
        time.sleep(0.01)
        dock3.execute_led()
        time.sleep(0.01)
        
except KeyboardInterrupt:
    cleanup_docks([dock1, dock2, dock3])

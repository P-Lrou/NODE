from tools.DLog import DLog
from rfid.Rfid import Rfid
from led.NeoLed import NeoLed

class Dock:
    def __init__(self, rfid_dock_callback=None) -> None:
        self.rfid = None
        self.rfid_dock_callback = rfid_dock_callback
        self.ring_led = None
        self.num_pixels = 24
        self.activity = None
        self.color_name = None

    def set_rfid(self, pin_number: int) -> None:
        if self.rfid_dock_callback is not None:
            self.rfid_dock_callback.set_dock(self)
        self.rfid = Rfid(pin_number, self.rfid_dock_callback)

    def set_ring_led(self, pin_number: int, num_pixels: int, starting_pixel: int = 0, total_pixels: int = 72) -> None:
        self.ring_led = NeoLed(pin_number, num_pixels, starting_pixel, total_pixels)

    def process(self) -> None:
        if self.rfid is not None:
            self.rfid.process()
        else:
            DLog.LogError("Error to process rfid! self.rfid is None")

    def has_activity(self, activity_type: str) -> bool:
        return self.activity == activity_type
        
    def launch_circle(self):
        if self.ring_led is not None:
            self.ring_led.circle((0, 255, 0), wait=0)
        else:
            DLog.LogError("Error: self.ring_led is None")

    def launch_pulse(self):
        if self.ring_led is not None:
            self.ring_led.pulse((0, 0, 255), wait=0)
        else:
            DLog.LogError("Error: self.ring_led is None")

    def launch_fill(self):
        if self.ring_led is not None:
            self.ring_led.fill((255, 0, 0))
        else:
            DLog.LogError("Error: self.ring_led is None")

    def launch_stop(self):
        if self.ring_led is not None:
            self.ring_led.stop()
        else:
            DLog.LogError("Error: self.ring_led is None")

    def execute_led(self):
        if self.ring_led is not None:
            self.ring_led.execute()

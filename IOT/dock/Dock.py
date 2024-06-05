from tools.DLog import DLog
from tools.Color import Color
from rfid.Rfid import Rfid
from led.NeoLed import NeoLed

class Dock:
    def __init__(self, rfid_dock_callback=None) -> None:
        self.rfid = None
        self.rfid_dock_callback = rfid_dock_callback
        self.ring_led = None
        self.activity = None
        self.color_name = None

    def set_rfid(self, pin_number: int) -> None:
        self.rfid = Rfid(pin_number, self.rfid_dock_callback, parent=self)

    def set_ring_led(self, pin_number: int, num_pixels: int, starting_pixel: int = 0, total_pixels: int = 72) -> None:
        self.ring_led = NeoLed(pin_number, num_pixels, starting_pixel, total_pixels)

    def process(self) -> None:
        if self.rfid is not None:
            self.rfid.process()
            if self.ring_led is not None:
                self.ring_led.execute()
            else:
                DLog.LogError("Error to execute ring_led! self.ring_led is None")
        else:
            DLog.LogError("Error to process rfid! self.rfid is None")

    def has_activity(self, activity_type: str) -> bool:
        return self.activity == activity_type
        
    def launch_circle(self):
        if self.ring_led is not None:
            self.ring_led.circle(Color.get_color_by_text(self.activity), wait=0)
        else:
            DLog.LogError("Error: self.ring_led is None")

    def launch_pulse(self):
        if self.ring_led is not None:
            self.ring_led.pulse(Color.get_color_by_text(self.activity), wait=0)
        else:
            DLog.LogError("Error: self.ring_led is None")

    def launch_fill(self):
        if self.ring_led is not None:
            self.ring_led.fill(Color.get_color_by_text(self.activity))
        else:
            DLog.LogError("Error: self.ring_led is None")

    def launch_error(self):
        if self.ring_led is not None:
            self.ring_led.pulse((255, 0, 0))
        else:
            DLog.LogError("Error: self.ring_led is None")
    
    def launch_success(self):
        if self.ring_led is not None:
            self.ring_led.pulse((0, 255, 0))
        else:
            DLog.LogError("Error: self.ring_led is None")

    def launch_stop(self):
        if self.ring_led is not None:
            self.ring_led.stop()
        else:
            DLog.LogError("Error: self.ring_led is None")

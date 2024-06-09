
#* TOOLS
from tools.DLog import DLog
from tools.Color import Color
from tools.Sound import PlaySound

#* DOCK
from dock.DockDelegate import DockDelegate
from dock.DockState import *

#* RFID
from dock.rfid.Rfid import Rfid
from dock.rfid.RfidDelegate import RfidDelegate
from dock.rfid.Badge import *

#* NEOLED
from dock.neoled.NeoLed import NeoLed

class Dock(RfidDelegate):
    def __init__(self, id: int, delegate: DockDelegate) -> None:
        self.id = id
        self.delegate = delegate
        self.state: DockState = OffState(self)
        self.rfid: Rfid = None
        self.ring_led: NeoLed = None
        self.sounds = {
            "rfid": {
                "placed": None,
                "removed": None
            }
        }
        self.sound_volume = 10
        self.activity_badge: ActivityBadge = None
        self._has_activity = False

    def set_state(self, state: DockState):
        self.state = state

    def set_rfid(self, pin_number: int) -> None:
        self.rfid = Rfid(pin_number, delegate=self)

    def set_ring_led(self, pin_number: int, num_pixels: int, starting_pixel: int = 0, total_pixels: int = 72) -> None:
        self.ring_led = NeoLed(pin_number, num_pixels, starting_pixel, total_pixels)
        self.ring_led.stop()

    def set_sounds(self, rfid_sounds):
        for key_sound, rfid_sound in zip(self.sounds["rfid"].keys(), rfid_sounds):
            self.sounds["rfid"][key_sound] = rfid_sound

    #* RFID PART

    def process(self) -> None:
        if self.rfid is not None:
            self.rfid.process()
        else:
            DLog.LogError("Error to process rfid! self.rfid is None")

    def rfid_placed(self, badge: Badge, rfid: Rfid):
        self.activity_badge = ActivityBadge(badge.id, badge.text)
        self._has_activity = True
        DLog.Log(f"{self.activity_badge.get_activity()} placed")
        PlaySound.play(self.sounds["rfid"]["placed"], volume=self.sound_volume)
        self.delegate.activity_added(self)

    def rfid_removed(self, rfid: Rfid):
        self._has_activity = False
        DLog.Log(f"{self.activity_badge.get_activity()} removed")
        PlaySound.play(self.sounds["rfid"]["removed"], volume=self.sound_volume)
        self.delegate.activity_removed(self)

    #* STATE PART

    def off(self):
        self.state.off()

    def on(self):
        self.state.on()

    def waiting(self):
        self.state.waiting()

    def searching(self):
        self.state.searching()

    def found(self):
        self.state.found()

    def not_found(self):
        self.state.not_found()

    #* REQUEST PART

    def has_activity(self) -> bool:
        return self._has_activity

    def has_activity_type(self, activity_type: str) -> bool:
        if not self.has_activity():
            return False
        return activity_type == self.activity_badge.get_activity()
    
    def is_requestable(self):
        return isinstance(self.state, OnState)
    
    def is_cancelable(self):
        return isinstance(self.state, SearchingState)
        
    #* NEOLED PART

    def launch_circle(self):
        if self.ring_led is not None:
            self.ring_led.circle(Color.get_color_by_text(self.activity_badge.get_activity()), wait=0.1)
        else:
            DLog.LogError("Error: self.ring_led is None")

    def launch_pulse(self):
        if self.ring_led is not None:
            self.ring_led.pulse(Color.get_color_by_text(self.activity_badge.get_activity()), wait=0.01)
        else:
            DLog.LogError("Error: self.ring_led is None")

    def launch_fill(self):
        if self.ring_led is not None:
            self.ring_led.fill(Color.get_color_by_text(self.activity_badge.get_activity()), brightness=1)
        else:
            DLog.LogError("Error: self.ring_led is None")

    def launch_error(self):
        if self.ring_led is not None:
            self.ring_led.pulse((255, 0, 0), wait=0.01)
        else:
            DLog.LogError("Error: self.ring_led is None")
    
    def launch_success(self):
        if self.ring_led is not None:
            self.ring_led.pulse(Color.get_color_by_text(self.activity_badge.get_activity()), wait=0.001)
        else:
            DLog.LogError("Error: self.ring_led is None")

    def launch_wait(self):
        if self.ring_led is not None:
            self.ring_led.pulse((255, 255, 255), wait=0.03)
        else:
            DLog.LogError("Error: self.ring_led is None")

    def launch_stop(self):
        if self.ring_led is not None:
            self.ring_led.stop()
        else:
            DLog.LogError("Error: self.ring_led is None")

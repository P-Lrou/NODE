from GlobalVariables import *
from dock.Dock import Dock

class DockController:
    def __init__(self, rfid_dock_callback=None) -> None:
        self.docks: list[Dock] = []
        rfid_pins = RfidPins.instance().rfid_number
        nums_pixels = NeoLedPins.instance().nums_pixels
        if len(rfid_pins) != len(nums_pixels):
            DLog.LogError("No matching number between rfid_pins and nums_pixels")
        else:
            for key, rfid_pin, num_pixels in zip(range(len(nums_pixels)), rfid_pins, nums_pixels):
                dock = Dock(rfid_dock_callback)
                dock.set_rfid(rfid_pin)
                dock.set_ring_led(NeoLedPins.instance().pin_number, num_pixels, starting_pixel=key * num_pixels, total_pixels=NeoLedPins.instance().total_pixels)
                self.docks.append(dock)

    def process(self) -> None:
        for dock in self.docks:
            dock.process()

    def get_dock_by_activity(self, activity_type: str) -> Dock:
        for dock in self.docks:
            if dock.has_activity(activity_type):
                return dock
        return None
    
    def get_docks_by_non_activity(self, activity_type: str) -> list:
        valid_docks: list[Dock] = []
        for dock in self.docks:
            if not dock.has_activity(activity_type):
                valid_docks.append(dock)
        return valid_docks

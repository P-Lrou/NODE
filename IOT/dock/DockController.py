from GlobalVariables import *
from dock.Dock import Dock


class DockController:
    def __init__(self, rfid_dock_callback=None) -> None:
        self.docks: list[Dock] = []
        rfid_pins = RfidPins.instance().rfid_number
        neo_led_pins = NeoLedPins.instance().pin_number
        if len(rfid_pins) != len(neo_led_pins):
            DLog.LogError("No matching number between rfid_pins and neo_led_pins")
        else:
            for rfid_pin, neo_led_pin in zip(rfid_pins, neo_led_pins):
                dock = Dock(rfid_dock_callback)
                dock.set_rfid(rfid_pin)
                dock.set_ring_led(neo_led_pin)
                self.docks.append(dock)

    def process(self) -> None:
        for dock in self.docks:
            dock.process()
            time.sleep(0.001)

    def get_dock_by_activity(self, activity_type: str) -> Dock:
        for dock in self.docks:
            if dock.has_activity(activity_type):
                return dock
        return None

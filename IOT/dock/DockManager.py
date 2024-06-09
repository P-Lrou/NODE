from typing import TYPE_CHECKING
from GlobalVariables import *
from dock.Dock import Dock
from dock.DockDelegate import DockDelegate
from dock.DockManagerState import *
from wsclient.WSManager import WSManager

class DockManager(DockDelegate):            
    def __init__(self, ws_manager: WSManager) -> None:
        self.ws_manager = ws_manager
        self.state = EmptyDockManager(self)
        self.docks: list[Dock] = []
        rfid_pins = RfidPins.instance().rfid_number
        nums_pixels = NeoLedPins.instance().nums_pixels
        sounds = Path.instance().rfid_sounds

        if len(rfid_pins) != len(nums_pixels):
            DLog.LogError("No matching number between rfid_pins and nums_pixels")
        else:
            for key, rfid_pin, num_pixels, sound in zip(range(len(nums_pixels)), rfid_pins, nums_pixels, sounds):
                self.dock_changed.append(False)
                dock = Dock(delegate=self)
                dock.set_rfid(rfid_pin)
                dock.set_ring_led(NeoLedPins.instance().pin_number, num_pixels, starting_pixel=key * num_pixels, total_pixels=NeoLedPins.instance().total_pixels)
                dock.set_sounds([sound])
                self.docks.append(dock)
    
    def set_state(self, state: DockManagerState):
        DLog.LogWhisper(f"Passing to {state.__class__.__name__} state")
        self.state = state

    def activity_added(self, dock: Dock) -> None:
        self.state.activity_added(dock)

    def activity_removed(self, dock: Dock) -> None:
        self.state.activity_removed(dock)

    def has_active_dock(self) -> bool:
        for dock in self.docks:
            if dock.has_activity():
                return True
        return False
    
    def has_searching_dock(self) -> bool:
        for dock in self.docks:
            if dock.is_searching():
                return True
        return False

    def process(self) -> None:
        for dock in self.docks:
            dock.process()

    def stop_all(self) -> None:
        for dock in self.docks:
            dock.off()

    def request_activities(self) -> None:
        activities_type: list[str] = [dock for dock in self.docks if dock.is_requestable()]
        if len(activities_type) > 0:
            self.ws_manager.send_activities_request(activities_type)
        else:
            DLog.LogWarning("Any dock are requestable")
    
    def cancel_activity(self, dock: Dock) -> None:
        activity_type = dock.activity_badge.get_activity()
        if dock.is_cancelable():
            self.ws_manager.send_activities_cancel([activity_type])
        else:
            DLog.LogWarning("The dock is not cancelable")

    def cancel_activities(self) -> None:
        activities_type: list[str] = [dock for dock in self.docks if dock.is_cancelable()]
        if len(activities_type) > 0:
            self.ws_manager.send_activities_cancel(activities_type)
        else:
            DLog.LogWarning("Any dock are cancelable")
    
    def handle_activities(self) -> None:
        self.state.handle_activities()
    
    def activity_search(self, activity_type: str) -> None:
        self.state.activity_search(activity_type)
    
    def activity_cancel(self, activity_type: str) -> None:
        self.state.activity_cancel(activity_type)

    def activity_found(self, activity_type: str) -> None:
        self.state.activity_found(activity_type)

    def activity_not_found(self, activity_type: str) -> None:
        self.state.activity_not_found(activity_type)


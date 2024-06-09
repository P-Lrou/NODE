from typing import TYPE_CHECKING
from GlobalVariables import *
from dock.Dock import Dock
from dock.DockDelegate import DockDelegate
from wsclient.WSManager import WSManager

class DockManager(DockDelegate):            
    def __init__(self, ws_manager: WSManager) -> None:
        self.ws_manager = ws_manager
        self.docks: list[Dock] = []
        self.dock_changed = []
        rfid_pins = RfidPins.instance().rfid_number
        nums_pixels = NeoLedPins.instance().nums_pixels
        sounds = Path.instance().rfid_sounds

        if len(rfid_pins) != len(nums_pixels):
            DLog.LogError("No matching number between rfid_pins and nums_pixels")
        else:
            for key, rfid_pin, num_pixels, sound in zip(range(len(nums_pixels)), rfid_pins, nums_pixels, sounds):
                self.dock_changed.append(False)
                dock = Dock(key, delegate=self)
                dock.set_rfid(rfid_pin)
                dock.set_ring_led(NeoLedPins.instance().pin_number, num_pixels, starting_pixel=key * num_pixels, total_pixels=NeoLedPins.instance().total_pixels)
                dock.set_sounds([sound])
                self.docks.append(dock)

    def activity_added(self, dock: Dock) -> None:
        self.dock_changed[dock.id] = True
        dock.on()
        for other_dock in self.docks:
            if other_dock != dock and not other_dock.has_activity():
                other_dock.waiting()

    def activity_removed(self, dock: Dock) -> None:
        self.dock_changed[dock.id] = False
        if self.has_active_dock():
            dock.waiting()
        else:
            for a_dock in self.docks:
                a_dock.off()

    def has_active_dock(self) -> bool:
        for dock in self.docks:
            if dock.has_activity():
                return True
        return False

    def process(self) -> None:
        for dock in self.docks:
            dock.process()

    def stop_all(self) -> None:
        for dock in self.docks:
            dock.off()

    def has_new_requests(self):
        return True in self.dock_changed
    
    def reset_dock_changed(self):
        self.dock_changed = [False for _ in self.dock_changed]

    def requested_activities(self) -> list[str]:
        activities: list[str] = []
        for dock in self.docks:
            if dock.has_activity() and dock.is_requestable():
                activities.append(dock.activity_badge.get_activity())
        return activities
    
    def canceled_activities(self) -> list[str]:
        activities: list[str] = []
        for dock in self.docks:
            if dock.has_activity() and dock.is_cancelable():
                activities.append(dock.activity_badge.get_activity())
        return activities
    
    def handle_activities(self) -> None:
        if self.has_new_requests():
            activities_type = self.requested_activities()
            self.ws_manager.send_activities_request(activities_type)
        else:
            activities_type = self.canceled_activities()
            self.ws_manager.send_activities_cancel(activities_type)
        self.reset_dock_changed()
        
    
    def activity_join(self, activity_type: str) -> None:
        for dock in self.docks:
            if dock.has_activity_type(activity_type):
                dock.searching()
            else:
                dock.off()
    
    def activity_leave(self, activity_type: str) -> None:
        for dock in self.docks:
            if dock.has_activity_type(activity_type):
                dock.off()

    def activity_found(self, activity_type: str) -> None:
        for dock in self.docks:
            if dock.has_activity_type(activity_type):
                dock.found()
            else:
                dock.off()
    
    def activity_not_found(self, activity_type: str) -> None:
        for dock in self.docks:
            if dock.has_activity_type(activity_type):
                dock.not_found()


    #********** A VOIR

    def get_docks_by_activity(self, activity_type: str) -> Dock:
        valid_docks: list[Dock] = []
        for dock in self.docks:
            if dock.has_activity(activity_type):
                valid_docks.append(dock)
        return valid_docks
    
    def get_docks_by_non_activity(self, activity_type: str) -> list:
        valid_docks: list[Dock] = []
        for dock in self.docks:
            if not dock.has_activity(activity_type):
                valid_docks.append(dock)
        return valid_docks

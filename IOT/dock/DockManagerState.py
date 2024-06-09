from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dock.DockManager import DockManager
    from dock.Dock import Dock

from tools.DLog import DLog
from tools.Timer import Timer

class DockManagerState:
    def __init__(self, dock_manager: "DockManager") -> None:
        self.dock_manager = dock_manager
        self.debug = True

    def __cant_change_state(self, next_class_name):
        class_name = self.__class__.__name__
        if self.debug and class_name != next_class_name:
            DLog.LogWarning(f"Can't change {class_name} state to {next_class_name} state")

    def activity_added(self, dock: "Dock") -> None:
        next_class_name = AddingDockManager.__name__
        self.__cant_change_state(next_class_name)
    
    def activity_removed(self, dock: "Dock") -> None:
        next_class_name = EmptyDockManager.__name__
        self.__cant_change_state(next_class_name)

    def handle_activities(self) -> None:
        pass
    
    def activity_search(self, activity_type: str) -> None:
        next_class_name = SearchingDockManager.__name__
        self.__cant_change_state(next_class_name)

    def activity_cancel(self, activity_type: str) -> None:
        pass

    def activity_found(self, activity_type: str) -> None:
        next_class_name = FoundDockManager.__name__
        self.__cant_change_state(next_class_name)

    def activity_not_found(self, activity_type: str) -> None:
        pass

    def _empty(self) -> None:
        for dock in self.dock_manager.docks:
            dock.off()
        self.dock_manager.set_state(EmptyDockManager(self.dock_manager))

    def _searching(self, activity_type: str) -> None:
        has_search = False
        for dock in self.dock_manager.docks:
            if dock.is_requestable() or dock.is_searching():
                if dock.has_activity_type(activity_type):
                    has_search = True
                    dock.searching()
            else:
                dock.off()
        if has_search and not isinstance(self, SearchingDockManager):
            self.dock_manager.set_state(SearchingDockManager(self.dock_manager))
        else:
            next_class_name = SearchingDockManager.__name__
            self.__cant_change_state(next_class_name)

    def _cancel(self, activity_type: str) -> None:
        for dock in self.dock_manager.docks:
            if dock.is_cancelable() and dock.has_activity_type(activity_type):
                dock.off()
        if not self.dock_manager.has_searching_dock():
            self.dock_manager.set_state(WaitingDockManager(self.dock_manager))

    def _found(self, activity_type: str) -> None:
        has_found = False
        for dock in self.dock_manager.docks:
            if dock.is_foundable():
                if dock.has_activity_type(activity_type):
                    dock.found()
                    has_found = True
                else:
                    dock.off()
            else:
                dock.off()
        if has_found:
            self.dock_manager.set_state(FoundDockManager(self.dock_manager))
        else:
            next_class_name = FoundDockManager.__name__
            self.__cant_change_state(next_class_name)
    
    def _not_found(self, activity_type: str) -> None:
        for dock in self.dock_manager.docks:
            if dock.is_foundable():
                if dock.has_activity_type(activity_type):
                    dock.not_found()

    def _waiting(self) -> None:
        for dock in self.dock_manager.docks:
            dock.waiting()
        self.dock_manager.set_state(WaitingDockManager(self.dock_manager))

# WHEN AN ACTIVITY IS PLACED
class AddingDockManager(DockManagerState):
    def __init__(self, dock_manager: "DockManager") -> None:
        super().__init__(dock_manager)

    def activity_added(self, dock: "Dock") -> None:
        dock.on()

    def activity_removed(self, dock: "Dock") -> None:
        self.dock_manager.cancel_activity(dock)
        if self.dock_manager.has_active_dock():
            dock.suggesting()
        else:
            self._empty()

    def handle_activities(self) -> None:
        self.dock_manager.request_activities()

    def activity_search(self, activity_type: str) -> None:
        self._searching(activity_type)

    def activity_cancel(self, activity_type: str) -> None:
        self._cancel(activity_type)

    def activity_found(self, activity_type: str) -> None:
        self._found(activity_type)

    def activity_not_found(self, activity_type: str) -> None:
        self._not_found(activity_type)

# WHEN NO ACTIVITIES ARE PLACED
class EmptyDockManager(DockManagerState):
    def __init__(self, dock_manager: "DockManager") -> None:
        super().__init__(dock_manager)

    def activity_added(self, dock: "Dock") -> None:
        for other_dock in self.dock_manager.docks:
            if other_dock == dock:
                other_dock.on()
            else:
                other_dock.suggesting()
        self.dock_manager.set_state(AddingDockManager(self.dock_manager))

# WHEN SENDING REQUEST, PASSED TO SEARCHING
class SearchingDockManager(DockManagerState):
    def __init__(self, dock_manager: "DockManager") -> None:
        super().__init__(dock_manager)

    def activity_added(self, dock: "Dock") -> None:
        dock.on()
        self.dock_manager.set_state(AddingDockManager(self.dock_manager))

    def activity_removed(self, dock: "Dock") -> None:
        self.dock_manager.cancel_activity(dock)
        if self.dock_manager.has_active_dock():
            dock.off()
        else:
            self._empty()

    def handle_activities(self) -> None:
        self.dock_manager.cancel_activities()

    def activity_search(self, activity_type: str) -> None:
        self._searching(activity_type)

    def activity_cancel(self, activity_type: str) -> None:
        self._cancel(activity_type)

    def activity_found(self, activity_type: str) -> None:
        self._found(activity_type)

    def activity_not_found(self, activity_type: str) -> None:
        self._not_found(activity_type)

# WHEN AN ACTIVITY IS FOUND
class FoundDockManager(DockManagerState):
    def __init__(self, dock_manager: "DockManager") -> None:
        super().__init__(dock_manager)
        time_before_waiting = 2
        Timer.instance("dock_manager").start(time_before_waiting, self._waiting)

    def activity_added(self, dock: "Dock") -> None:
        for other_dock in self.dock_manager.docks:
            if other_dock == dock:
                dock.on()
            else:
                if other_dock.has_activity():
                    other_dock.on()
                else:
                    other_dock.suggesting()
        self.dock_manager.set_state(AddingDockManager(self.dock_manager))

    def activity_removed(self, dock: "Dock") -> None:
        if self.dock_manager.has_active_dock():
            dock.off()
        else:
            self._empty()

# AFTER ACTIVITY FOUND, WHEN NOTHING HAPPENS
class WaitingDockManager(DockManagerState):
    def __init__(self, dock_manager: "DockManager") -> None:
        super().__init__(dock_manager)

    def activity_added(self, dock: "Dock") -> None:
        for other_dock in self.dock_manager.docks:
            if other_dock == dock:
                other_dock.on()
            else:
                if other_dock.has_activity():
                    other_dock.on()
                else:
                    other_dock.suggesting()
        self.dock_manager.set_state(AddingDockManager(self.dock_manager))

    def activity_removed(self, dock: "Dock") -> None:
        if not self.dock_manager.has_active_dock():
            self._empty()

    def handle_activities(self) -> None:
        self.dock_manager.request_activities()

    def activity_search(self, activity_type: str) -> None:
        self._searching(activity_type)
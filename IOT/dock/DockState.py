from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dock.Dock import Dock

from tools.DLog import DLog

class DockState:
    def __init__(self, dock: "Dock") -> None:
        self.dock = dock
        self.debug = True

    def __cant_change_state(self, next_class_name):
        class_name = self.__class__.__name__
        if self.debug and class_name != next_class_name:
            DLog.LogWarning(f"Can't change {class_name} state to {next_class_name} state")

    def off(self):
        next_class_name = DockOff.__name__
        self.__cant_change_state(next_class_name)

    def on(self):
        next_class_name = DockOn.__name__
        self.__cant_change_state(next_class_name)

    def suggesting(self):
        next_class_name = DockSuggesting.__name__
        self.__cant_change_state(next_class_name)

    def searching(self):
        next_class_name = DockSearching.__name__
        self.__cant_change_state(next_class_name)

    def found(self):
        next_class_name = DockFound.__name__
        self.__cant_change_state(next_class_name)

    def not_found(self):
        next_class_name = DockNotFound.__name__
        self.__cant_change_state(next_class_name)
    
    def waiting(self):
        next_class_name = DockWaiting.__name__
        self.__cant_change_state(next_class_name)

    def _off(self):
        self.dock.launch_stop()
        self.dock.set_state(DockOff(self.dock))
    
    def _on(self):
        self.dock.launch_fill()
        self.dock.set_state(DockOn(self.dock))
    
    def _suggesting(self):
        self.dock.launch_wait()
        self.dock.set_state(DockSuggesting(self.dock))
    
    def _searching(self):
        self.dock.launch_circle()
        self.dock.set_state(DockSearching(self.dock))
    
    def _found(self):
        self.dock.launch_success()
        self.dock.set_state(DockFound(self.dock))

    def _not_found(self):
        self.dock.launch_stop()
        self.dock.set_state(DockNotFound(self.dock))

    def _waiting(self):
        self.dock.launch_stop()
        self.dock.set_state(DockWaiting(self.dock))

 
class DockOff(DockState):
    def __init__(self, dock: "Dock") -> None:
        super().__init__(dock)

    def on(self):
        self._on()

    def suggesting(self):
        self._suggesting()

    def waiting(self):
        self._waiting()

class DockOn(DockState):
    def __init__(self, dock: "Dock") -> None:
        super().__init__(dock)

    def off(self):
        self._off()

    def suggesting(self):
        self._suggesting()

    def searching(self):
        self._searching()

class DockSuggesting(DockState):
    def __init__(self, dock: "Dock") -> None:
        super().__init__(dock)

    def off(self):
        self._off()

    def on(self):
        self._on()

class DockSearching(DockState):
    def __init__(self, dock: "Dock") -> None:
        super().__init__(dock)

    def off(self):
        self._off()

    def suggesting(self):
        self._off()

    def found(self):
        self._found()

    def not_found(self):
        self._not_found()

    def waiting(self):
        self._waiting()

class DockFound(DockState):
    def __init__(self, dock: "Dock") -> None:
        super().__init__(dock)

    def on(self):
        self._on()

    def off(self):
        self._off()

    def searching(self):
        self._searching()

    def waiting(self):
        self._waiting()

class DockNotFound(DockState):
    def __init__(self, dock: "Dock") -> None:
        super().__init__(dock)

    def off(self):
        self._off()

    def searching(self):
        self._searching()

    def waiting(self):
        self._waiting()

class DockWaiting(DockState):
    def __init__(self, dock: "Dock") -> None:
        super().__init__(dock)

    def off(self):
        self._off()

    def on(self):
        self._on()

    def suggesting(self):
        self._suggesting()

    def searching(self):
        self._searching()

    
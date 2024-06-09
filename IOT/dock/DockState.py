from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dock.Dock import Dock

from tools.DLog import DLog

class DockState:
    def __init__(self, dock: "Dock") -> None:
        self.dock = dock
        self.debug = True

    def off(self):
        class_name = self.__class__.__name__
        if self.debug and class_name != "OffState":
            DLog.LogWarning(f"Can't change {class_name} to OffState")

    def on(self):
        class_name = self.__class__.__name__
        if self.debug and class_name != "OnState":
            DLog.LogWarning(f"Can't change {class_name} to OnState")

    def waiting(self):
        class_name = self.__class__.__name__
        if self.debug and class_name != "WaitingState":
            DLog.LogWarning(f"Can't change {class_name} to WaitingState")

    def searching(self):
        class_name = self.__class__.__name__
        if self.debug and class_name != "SearchingState":
            DLog.LogWarning(f"Can't change {class_name} to SearchingState")

    def found(self):
        class_name = self.__class__.__name__
        if self.debug and class_name != "FoundState":
            DLog.LogWarning(f"Can't change {class_name} to FoundState")

    def not_found(self):
        class_name = self.__class__.__name__
        if self.debug and class_name != "NotFoundState":
            DLog.LogWarning(f"Can't change {class_name} to NotFoundState")

    def _off(self):
        self.dock.launch_stop()
        self.dock.set_state(OffState(self.dock))
    
    def _on(self):
        self.dock.launch_fill()
        self.dock.set_state(OnState(self.dock))
    
    def _waiting(self):
        self.dock.launch_wait()
        self.dock.set_state(WaitingState(self.dock))
    
    def _searching(self):
        self.dock.launch_circle()
        self.dock.set_state(SearchingState(self.dock))
    
    def _found(self):
        self.dock.launch_success()
        self.dock.set_state(FoundState(self.dock))

    def _not_found(self):
        self.dock.launch_stop()
        self.dock.set_state(NotFoundState(self.dock))
 
class OffState(DockState):
    def __init__(self, dock: "Dock") -> None:
        super().__init__(dock)

    def on(self):
        self._on()

    def waiting(self):
        self._waiting()

class OnState(DockState):
    def __init__(self, dock: "Dock") -> None:
        super().__init__(dock)

    def off(self):
        self._off()

    def waiting(self):
        self._waiting()

    def searching(self):
        self._searching()

class WaitingState(DockState):
    def __init__(self, dock: "Dock") -> None:
        super().__init__(dock)

    def off(self):
        self._off()

    def on(self):
        self._on()

class SearchingState(DockState):
    def __init__(self, dock: "Dock") -> None:
        super().__init__(dock)

    def off(self):
        self._off()

    def found(self):
        self._found()

    def not_found(self):
        self._not_found()

class FoundState(DockState):
    def __init__(self, dock: "Dock") -> None:
        super().__init__(dock)

    def off(self):
        self._off()

    def searching(self):
        self._searching()

class NotFoundState(DockState):
    def __init__(self, dock: "Dock") -> None:
        super().__init__(dock)

    def off(self):
        self._off()

    def searching(self):
        self._searching()

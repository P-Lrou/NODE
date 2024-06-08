from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dock.Dock import Dock

class DockState:
    def __init__(self, dock: "Dock") -> None:
        self.dock = dock

    def off(self):
        pass

    def on(self):
        pass

    def waiting(self):
        pass

    def searching(self):
        pass

    def found(self):
        pass

    def not_found(self):
        pass

    def idle(self):
        pass
    
class OffState(DockState):
    def __init__(self, dock: Dock) -> None:
        super().__init__(dock)

class OnState(DockState):
    def __init__(self, dock: Dock) -> None:
        super().__init__(dock)

class WaitingState(DockState):
    def __init__(self, dock: Dock) -> None:
        super().__init__(dock)

class SearchingState(DockState):
    def __init__(self, dock: Dock) -> None:
        super().__init__(dock)

class FoundState(DockState):
    def __init__(self, dock: Dock) -> None:
        super().__init__(dock)

class NotFoundState(DockState):
    def __init__(self, dock: Dock) -> None:
        super().__init__(dock)

class IdleState(DockState):
    def __init__(self, dock: Dock) -> None:
        super().__init__(dock)
        
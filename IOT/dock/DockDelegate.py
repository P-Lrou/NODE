from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dock.Dock import Dock

class DockDelegate:
    def __init__(self) -> None:
        pass

    def activity_added(self, dock: "Dock") -> None:
        pass

    def activity_removed(self, dock: "Dock") -> None:
        pass
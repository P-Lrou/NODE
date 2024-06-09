from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from button.Button import Button

class ButtonDelegate:
    def __init__(self) -> None:
        pass

    def on_clicked(self, button: "Button") -> None:
        pass
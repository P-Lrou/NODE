from GlobalVariables import Activities
from tools.DLog import DLog

class Badge:
    def __init__(self, id, text) -> None:
        self.id: str = id
        self.text: str = text
        
class ActivityBadge(Badge):
    def __init__(self, id, text) -> None:
        super().__init__(id, text)
        self._known_activity = True
        activities = Activities.instance().activities
        data: list[str] = self.text.split(":")
        self.activity = data[0]
        if self.activity not in activities:
            self._known_activity = False
            DLog.LogError(f"Unkown activity. Text: '{self.activity}'")

    def is_known(self):
        return self._known_activity

    def get_activity(self) -> str:
        return self.activity if self._known_activity else None
    
    def get_color(self) -> str:
        data: list[str] = self.text.split(":")
        color_name = ""
        if len(data) > 1:
            color_name = data[1]
        return color_name
from tools.DLog import DLog

class LedPins:
    _instance = None

    def __init__(self):
        self.matchmaking_number = [6, 13, 19, 26]
        self.activities_number = [17, 27, 22, 23, 5, 0]
        self.activities_led_number = {}
        activities = Activities.instance().activities
        if len(self.activities_number) == len(activities):
            for i in range(0, len(activities)):
                self.activities_led_number[activities[i]] = self.activities_number[i]
        else:
            DLog.LogError("No matching length between activities_number and activities")

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


class Activities:
    _instance = None

    def __init__(self):
        self.activities = [
            "belotte",
            "echecs",
            "scrabble",
            "tarot",
            "bridge",
            "balade"
        ]

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
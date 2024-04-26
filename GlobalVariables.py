
class LedPins:
    _instance = None

    def __init__(self):
        self.matchmaking_number = [6, 13, 19, 26]
        self.activities_number = [17, 27, 22]
        self.activities_led_number = {}
        if len(self.activities_number) == len(Activities.instance.activities):
            for i in range(0, len(Activities.instance.activities)):
                self.activities_led_number[Activities.instance.activities[i]] = self.activities_number[i]
        else:
            print("No matching length between activities_number and activities")

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
            "scrabble"
        ]

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

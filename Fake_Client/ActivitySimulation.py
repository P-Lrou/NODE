import json

class ActivityBuilder:
    def __init__(self) -> None:
        pass

    @staticmethod
    def type():
        return {
            "type": "activity"
        }
    
    @staticmethod
    def add_state():
        return {
            "state": "request"
        }
    
    @staticmethod
    def remove_state():
        return {
            "state": "retire"
        }
    
    @staticmethod
    def set_activity(activities):
        return {
            "activities_type": activities
        }
    
    def merge_data(type, state, activity):
        return {
            **type,
            **state,
            **activity
        }

class ActivitySimulation:
    BELOTE = "belote"
    SCRABBLE = "scrabble"
    GOUTER = "gouter"
    PROMENADE = "promenade"
    PETANUE = "petanue"
    TRIOMINO = "triomino"
    def __init__(self) -> None:
        pass

    @staticmethod
    def add(activities):
        data = ActivityBuilder.merge_data(
            ActivityBuilder.type(),
            ActivityBuilder.add_state(),
            ActivityBuilder.set_activity(activities)
        )
        return data
    
    @staticmethod
    def remove(activities):
        data = ActivityBuilder.merge_data(
            ActivityBuilder.type(),
            ActivityBuilder.remove_state(),
            ActivityBuilder.set_activity(activities)
        )
        return data
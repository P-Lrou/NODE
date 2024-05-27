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
    def set_activity(activity):
        return {
            "activity_type": activity
        }
    
    def merge_data(type, state, activity):
        return {
            **type,
            **state,
            **activity
        }

class ActivitySimulation:
    def __init__(self) -> None:
        pass

    @staticmethod
    def add_belote():
        data = ActivityBuilder.merge_data(
            ActivityBuilder.type(),
            ActivityBuilder.add_state(),
            ActivityBuilder.set_activity("belote")
        )
        return data
    
    @staticmethod
    def remove_belote():
        data = ActivityBuilder.merge_data(
            ActivityBuilder.type(),
            ActivityBuilder.remove_state(),
            ActivityBuilder.set_activity("belote")
        )
        return data
    
    @staticmethod
    def add_scrabble():
        data = ActivityBuilder.merge_data(
            ActivityBuilder.type(),
            ActivityBuilder.add_state(),
            ActivityBuilder.set_activity("scrabble")
        )
        return data
    
    @staticmethod
    def remove_scrabble():
        data = ActivityBuilder.merge_data(
            ActivityBuilder.type(),
            ActivityBuilder.remove_state(),
            ActivityBuilder.set_activity("scrabble")
        )
        return data
    
    @staticmethod
    def add_gouter():
        data = ActivityBuilder.merge_data(
            ActivityBuilder.type(),
            ActivityBuilder.add_state(),
            ActivityBuilder.set_activity("gouter")
        )
        return data
    
    @staticmethod
    def remove_gouter():
        data = ActivityBuilder.merge_data(
            ActivityBuilder.type(),
            ActivityBuilder.remove_state(),
            ActivityBuilder.set_activity("gouter")
        )
        return data
    
    @staticmethod
    def add_promenade():
        data = ActivityBuilder.merge_data(
            ActivityBuilder.type(),
            ActivityBuilder.add_state(),
            ActivityBuilder.set_activity("promenade")
        )
        return data
    
    @staticmethod
    def remove_promenade():
        data = ActivityBuilder.merge_data(
            ActivityBuilder.type(),
            ActivityBuilder.remove_state(),
            ActivityBuilder.set_activity("promenade")
        )
        return data
    
    @staticmethod
    def add_petanque():
        data = ActivityBuilder.merge_data(
            ActivityBuilder.type(),
            ActivityBuilder.add_state(),
            ActivityBuilder.set_activity("petanque")
        )
        return data
    
    @staticmethod
    def remove_petanque():
        data = ActivityBuilder.merge_data(
            ActivityBuilder.type(),
            ActivityBuilder.remove_state(),
            ActivityBuilder.set_activity("petanque")
        )
        return data
    
    @staticmethod
    def add_triomino():
        data = ActivityBuilder.merge_data(
            ActivityBuilder.type(),
            ActivityBuilder.add_state(),
            ActivityBuilder.set_activity("triomino")
        )
        return data
    
    @staticmethod
    def remove_triomino():
        data = ActivityBuilder.merge_data(
            ActivityBuilder.type(),
            ActivityBuilder.remove_state(),
            ActivityBuilder.set_activity("triomino")
        )
        return data
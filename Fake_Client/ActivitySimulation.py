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
            "state": "joined"
        }
    
    @staticmethod
    def remove_state():
        return {
            "state": "retired"
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
    def add_belotte():
        data = ActivityBuilder.merge_data(
            ActivityBuilder.type(),
            ActivityBuilder.add_state(),
            ActivityBuilder.set_activity("belotte")
        )
        return json.dumps(data)
    
    @staticmethod
    def remove_belotte():
        data = ActivityBuilder.merge_data(
            ActivityBuilder.type(),
            ActivityBuilder.remove_state(),
            ActivityBuilder.set_activity("belotte")
        )
        return json.dumps(data)
    
    @staticmethod
    def add_scrabble():
        data = ActivityBuilder.merge_data(
            ActivityBuilder.type(),
            ActivityBuilder.add_state(),
            ActivityBuilder.set_activity("scrabble")
        )
        return json.dumps(data)
    
    @staticmethod
    def remove_scrabble():
        data = ActivityBuilder.merge_data(
            ActivityBuilder.type(),
            ActivityBuilder.remove_state(),
            ActivityBuilder.set_activity("scrabble")
        )
        return json.dumps(data)
    
    @staticmethod
    def add_echecs():
        data = ActivityBuilder.merge_data(
            ActivityBuilder.type(),
            ActivityBuilder.add_state(),
            ActivityBuilder.set_activity("echecs")
        )
        return json.dumps(data)
    
    @staticmethod
    def remove_echecs():
        data = ActivityBuilder.merge_data(
            ActivityBuilder.type(),
            ActivityBuilder.remove_state(),
            ActivityBuilder.set_activity("echecs")
        )
        return json.dumps(data)
    
    @staticmethod
    def add_tarot():
        data = ActivityBuilder.merge_data(
            ActivityBuilder.type(),
            ActivityBuilder.add_state(),
            ActivityBuilder.set_activity("tarot")
        )
        return json.dumps(data)
    
    @staticmethod
    def remove_tarot():
        data = ActivityBuilder.merge_data(
            ActivityBuilder.type(),
            ActivityBuilder.remove_state(),
            ActivityBuilder.set_activity("tarot")
        )
        return json.dumps(data)
    
    @staticmethod
    def add_bridge():
        data = ActivityBuilder.merge_data(
            ActivityBuilder.type(),
            ActivityBuilder.add_state(),
            ActivityBuilder.set_activity("bridge")
        )
        return json.dumps(data)
    
    @staticmethod
    def remove_bridge():
        data = ActivityBuilder.merge_data(
            ActivityBuilder.type(),
            ActivityBuilder.remove_state(),
            ActivityBuilder.set_activity("bridge")
        )
        return json.dumps(data)
    
    @staticmethod
    def add_balade():
        data = ActivityBuilder.merge_data(
            ActivityBuilder.type(),
            ActivityBuilder.add_state(),
            ActivityBuilder.set_activity("balade")
        )
        return json.dumps(data)
    
    @staticmethod
    def remove_balade():
        data = ActivityBuilder.merge_data(
            ActivityBuilder.type(),
            ActivityBuilder.remove_state(),
            ActivityBuilder.set_activity("balade")
        )
        return json.dumps(data)
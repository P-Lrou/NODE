import json


class ActivitiesManager:
    def __init__(self):
        self.activities = {}
        self.load_activities()

    def load_activities(self):
        try:
            with open("activities.json", "r") as file:
                self.activities = json.load(file)
        except FileNotFoundError:
            self.reset_activities()

    def reset_activities(self):
        self.activities = {
            "belotte": {"required_participants": 4, "participants": []},
            "scrabble": {"required_participants": 4, "participants": []},
            "echecs": {"required_participants": 2, "participants": []}
        }
        self.save_activities() 

    def save_activities(self):
        with open("activities.json", "w") as file:
            json.dump(self.activities, file, indent=4)

    def add_participant(self, data, client):
        activity_type = data.get('activity_type')
        if activity_type in self.activities:
            self.activities[activity_type]['participants'].append(
                {"id": client['id'], "uid": client["uid"]})
            self.save_activities()
            return activity_type
        return None
    
    def remove_participant(self, data, client):
        activity_type = data.get('activity_type')
        if activity_type in self.activities:
            self.activities[activity_type]['participants'].remove(
                {"id": client['id'], "uid": client["uid"]})
            self.save_activities()
            return activity_type
        return None

    def get_participants_count(self, activity_type):
        if activity_type in self.activities:
            return len(self.activities[activity_type]['participants'])
        return 0

    def check_activity_full(self, activity_type):
        if activity_type in self.activities:
            return len(self.activities[activity_type]['participants']) >= self.activities[activity_type]['required_participants']
        return False

    def get_participants(self, activity_type):
        if activity_type in self.activities:
            return self.activities[activity_type]['participants']
        return []

    def activity_exists(self, activity_type):
        return activity_type in self.activities and len(self.activities[activity_type]['participants']) > 0

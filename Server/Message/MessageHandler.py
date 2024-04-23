from Activities.ActivitiesManager import ActivitiesManager
import json


class MessageHandler:

    def __init__(self):
        self.activitiesManager = ActivitiesManager()

    def process_message(self, message, server, client):
        data = json.loads(message)
        if 'type' in data:
            if data['type'] == 'activity':
                if 'activity_type' in data:
                    if data['activity_type'] == 'chess':
                        self.activitiesManager.new_activity("chess")
                    elif data['activity_type'] == 'poker':
                        self.activitiesManager.new_activity("poker")
                    elif data['activity_type'] == 'sewing':
                        self.activitiesManager.new_activity("sewing")
                    else:
                        return {"error": "Unknown activity type"}
                else:
                    return {"error": "Activity type not specified"}
        else:
            return {"error": "Unknown message type"}

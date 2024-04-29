from Activities.ActivitiesManager import ActivitiesManager
import json

class MessageHandler:
    def __init__(self):
        self.activitiesManager = ActivitiesManager()
        self.activitiesManager.reset_activities()

    def process_message(self, message, server, client):
        data = json.loads(message)
        data_content = json.loads(data["text"])
        if 'type' in data_content and data_content['type'] == 'activity':
            activity_type = data_content.get('activity_type')
            if activity_type:
                is_new_activity = not self.activitiesManager.activity_exists(activity_type)
                activity_id = self.activitiesManager.handle_activity(data_content, client)
                if activity_id:
                    if is_new_activity:
                        creation_message = json.dumps({"type": "activity_created", "activity_type": activity_type})
                        for c in server.clients:
                            if c["id"] != client["id"]:
                                server.send_message(c, creation_message)

                    participants = self.activitiesManager.get_participants(activity_id)
                    participants_count = self.activitiesManager.get_participants_count(activity_id)
                    new_participant_message = json.dumps({"type": "new_participant", "activity_type": activity_id, "count": participants_count})
                    
                    # Notify all current participants that a new player has joined
                    for participant in participants:
                        # Find the client object corresponding to participant['id']
                        target_client = next((c for c in server.clients if c['id'] == participant["id"]), None)
                        if target_client:
                            server.send_message(target_client, new_participant_message)
                        
                    # If the activity is full, inform all participants
                    if self.activitiesManager.check_activity_full(activity_id):
                        complete_message = json.dumps({"type": "activity_full", "activity_type": activity_id})
                        for participant in participants:
                            target_client = next((c for c in server.clients if c['id'] == participant["id"]), None)
                            if target_client:
                                server.send_message(target_client, complete_message)
            else:
                server.send_message(client, json.dumps({"error": "Activity type not specified"}))
        else:
            server.send_message(client, json.dumps({"error": "Unknown message type"}))

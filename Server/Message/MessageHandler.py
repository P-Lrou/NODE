from Activities.ActivitiesManager import ActivitiesManager
from tools.DLog import DLog
import json

class MessageHandler:
    def __init__(self):
        self.activitiesManager = ActivitiesManager()
        self.activitiesManager.reset_activities()

    def process_message(self, message, server, client):
        data = json.loads(message)
        if "text" in data:
            if "{" in data["text"] and "}" in data["text"]:
                data_content = json.loads(data["text"])
                if 'type' in data_content and data_content['type'] == 'activity':
                    if 'activity_type' in data_content:
                        activity_type = data_content['activity_type']
                        if "state" in data_content:
                            if data_content["state"] == "joined":
                                if self.activitiesManager.add_participant(activity_type, client):
                                    # If this is an new activity
                                    if not self.activitiesManager.activity_exists(activity_type):
                                        creation_message = json.dumps({"type": "activity_created", "activity_type": activity_type})
                                        DLog.LogWhisper(f"New activity: {activity_type} => sending: {creation_message}")
                                        for c in server.clients:
                                            server.send_message(c, creation_message)

                                    # Send data for number of participant
                                    participants = self.activitiesManager.get_participants(activity_type)
                                    participants_count = self.activitiesManager.get_participants_count(activity_type)
                                    new_participant_message = json.dumps({"type": "new_participant", "activity_type": activity_type, "count": participants_count})
                                    DLog.LogWhisper(f"New participant to {activity_type} => sending: {new_participant_message}")
                                    for participant in participants:
                                        target_client = next((c for c in server.clients if c['id'] == participant["id"]), None)
                                        if target_client:
                                            server.send_message(target_client, new_participant_message)

                                    # If the activity is full
                                    if self.activitiesManager.check_activity_full(activity_type):
                                        complete_message = json.dumps({"type": "activity_full", "activity_type": activity_type})
                                        DLog.LogWhisper(f"Activity {activity_type} is full => sending: {complete_message}")
                                        for participant in participants:
                                            target_client = next((c for c in server.clients if c['id'] == participant["id"]), None)
                                            if target_client:
                                                server.send_message(target_client, complete_message)
                                else:
                                    DLog.LogError("Can't add participant to the activity")
                                    server.send_message(client, json.dumps({"error": "Can't add participant to the activity"}))

                            elif data_content["state"] == "retired":
                                if self.activitiesManager.remove_participant(activity_type, client):
                                    leave_message = json.dumps({"type": "activity_leave", "activity_type": activity_type})
                                    DLog.LogWhisper(f"A participant leave the activity {activity_type} => sending: {leave_message}")
                                    server.send_message(client, leave_message)

                                    # Send data for number of participant
                                    participants = self.activitiesManager.get_participants(activity_type)
                                    participants_count = self.activitiesManager.get_participants_count(activity_type)
                                    drop_participant_message = json.dumps({"type": "drop_participant", "activity_type": activity_type, "count": participants_count})
                                    DLog.LogWhisper(f"Drop participant to {activity_type} => sending: {drop_participant_message}")
                                    for participant in participants:
                                        target_client = next((c for c in server.clients if c['id'] == participant["id"]), None)
                                        if target_client:
                                            server.send_message(target_client, new_participant_message)

                                    # If the activity is empty
                                    if self.activitiesManager.check_activity_empty(activity_type):
                                        empty_message = json.dumps({"type": "activity_empty", "activity_type": activity_type})
                                        DLog.LogWhisper(f"Activity {activity_type} is full => sending: {complete_message}")
                                        for c in server.clients:
                                            server.send_message(c, empty_message)
                                else:
                                    DLog.LogError("Can't remove participant to the activity")
                                    server.send_message(client, json.dumps({"error": "Can't remove participant to the activity"}))
                            else:
                                DLog.LogError("Unknown state")
                                server.send_message(client, json.dumps({"error": "Unknown state"}))
                        else:
                            DLog.LogError("There is no 'state' key")
                            server.send_message(client, json.dumps({"error": "There is no 'state' key"}))
                    else:
                        DLog.LogError("Activity type not specified")
                        server.send_message(client, json.dumps({"error": "Activity type not specified"}))
                else:
                    DLog.LogError("Unknown message type")
                    server.send_message(client, json.dumps({"error": "Unknown message type"}))
            else:
                DLog.LogError("'text' is not loadable to json")
                server.send_message(client, json.dumps({"error": "'text' is not loadable to json"}))
        else:
            DLog.LogError("There is not 'text' key in this message")
            server.send_message(client, json.dumps({"error": "There is not 'text' key in this message"}))

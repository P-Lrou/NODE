# TOOLS
from tools.DLog import DLog
from tools.JSONTools import *
# MODEL
from Model.BaseModel import BaseModel
from Model.Activity import Activity
from Model.Client import Client
from Model.Contact import Contact
from Model.Request import Request
from Model.Room import Room
from Model.Participant import Participant

class ActivitiesManager:
    def __init__(self):
        self.tables: list[BaseModel] = [
            Activity,
            Client,
            Contact,
            Request,
            Room,
            Participant
        ]
        self.tables_to_reset: list[BaseModel] = [
            Request,
            Client,
            Room,
            Participant
        ]

    def reset_database(self):
        for table in self.tables_to_reset:
            table.truncate_table()

    @staticmethod
    def create_groupe(activity: Activity) -> tuple[bool, dict]:
        room: Room = Room.insert(activity)
        if room:
            attempting_clients = activity.get_attempting_clients()
            for attempting_client in attempting_clients:
                request = attempting_client.get_attempting_request_by_activity(activity)
                if request:
                    request.update_state(Request.ACCEPTED)
                    participant: Participant = Participant.insert(attempting_client, room)
                    if participant:
                        targets = [attempting_client.uid for attempting_client in attempting_clients]
                        new_groupe = json_encode({"type": "found", "activity_type": activity.name, "rdv_at": str(room.get_rdv_time())})
                    else:
                        DLog.LogError(f"Error to insert a participant. Client id: {attempting_client}, Room id: {room}")
                        return False, {}
                else:
                    DLog.LogError(f"Request of activity client not found. Client id: {attempting_client}, Activity: {activity.name}")
                    return False, {}
                
            DLog.LogWhisper(f"New groupe: {activity.name}")
            return True, {
                "targets": targets,
                "message": new_groupe
            }
        else:
            DLog.LogError(f"Error to insert a room. Activity: {activity.name}")
        return False, {}

    @classmethod
    def looking_for_groupe(cls, client: Client) -> tuple[bool, dict]:
        requests = client.get_requests()
        number_by_activity: dict[Activity, int] = {request.activity: len(request.activity.get_requests()) for request in requests}
        sorted_number_by_activity = dict(sorted(number_by_activity.items(), key=lambda item: item[1], reverse=True))
        for activity in sorted_number_by_activity.keys():
            if activity.has_max_participants():
                return cls.create_groupe(activity)
            return False, {}
        DLog.LogError(f"No activity found")
        return False, {}

    @classmethod
    def new_request(cls, data: dict) -> list[dict]:
        data_to_send: list[dict] = []
        if "activity_type" in data: 
            activity_type = data["activity_type"]
            if "client_uid" in data: 
                activity: Activity = Activity.get_activity_by_name(activity_type)
                if activity:
                    client: Client = Client.get_first_client_by_uid(data["client_uid"])
                    if client:
                        attempting_request = client.get_attempting_request_by_activity(activity)
                        if not attempting_request:
                            request = Request.insert("", activity, client)
                            if request:
                                join_message = json_encode({"type": "join", "activity_type": activity_type})
                                join_targets = [data["client_uid"]]
                                data_to_send.append({
                                    "targets": join_targets,
                                    "message": join_message
                                })
                                DLog.LogWhisper(f"New join: {activity_type}")
                                request_message = json_encode({"type": "new_request", "activity_type": activity_type})
                                data_to_send.append({
                                    "targets": "all",
                                    "message": request_message
                                })
                                DLog.LogWhisper(f"New request: {activity_type}")
                                if "is_last" in data and data["is_last"] is True:
                                    has_groupe, new_data = cls.looking_for_groupe(client)
                                    if has_groupe:
                                        data_to_send.append(new_data)
                                return data_to_send
                            else:
                                message_error = "Error to insert a request"
                        else:
                            message_error = f"Request for activity {activity_type} already exist"
                    else:
                        message_error = f"No client found with uid: {data['client_uid']}"
                else:
                    message_error = f"No {data['activity_type']} activity found"
            else:
                message_error = "No 'client_uid' key in data"
        else:
            message_error = "No 'activity_type' in data"
        
        if not message_error:
            message_error = "THERE IS A BIG ERROR"
        data_to_send.append({
            "targets": [data["client_uid"]],
            "message": message_error
        })
        DLog.LogError(message_error)
        return data_to_send

    @staticmethod
    def cancel(data: dict) -> list[dict]:
        data_to_send: list[dict] = []
        if "activity_type" in data:
            activity_type = data["activity_type"]
            if "client_uid" in data:
                activity: Activity = Activity.get_activity_by_name(activity_type)
                if activity:
                    client: Client = Client.get_first_client_by_uid(data["client_uid"])
                    if client:
                        request = client.get_attempting_request_by_activity(activity)
                        if request:
                            request.update_state(Request.REFUSED)
                            leave_message = json_encode({"type": "leave", "activity_type": activity_type})
                            data_to_send.append({
                                "targets": [data["client_uid"]],
                                "message": leave_message
                            })
                            DLog.LogWhisper(f"Cancel request: {activity_type}")
                            return data_to_send
                        else:
                            message_error = f"Request of activity client not found. Client id: {client}, Activity: {activity.name}"
                    else:
                        message_error = f"No client found. Client id: {client}"
                else:
                    message_error = f"No {data['activity_type']} activity found"
            else:
                message_error = "No 'client_uid' key in data"
        else:
            message_error = "No 'activity_type' in data"
        
        if not message_error:
            message_error = "THERE IS A BIG ERROR"
        data_to_send.append({
            "targets": [data["client_uid"]],
            "message": message_error
        })
        DLog.LogError(message_error)
        return data_to_send

    @staticmethod
    def cancel_by_disconnection(client):
        client: Client = Client.get_first_client_by_uid(client["uid"])
        if client:
            requests = client.get_attempting_requests()
            for request in requests:
                request.update_state(Request.REFUSED)
            DLog.LogWhisper("Disconnection of a client, REFUSED all of his requests")
        else:
            DLog.LogError(f"No client found. uid: {client['uid']}")

    def check_requests_waiting_time(self, callback):
        data_to_send: list[dict] = []
        requests: list[Request] = Request.get_attempting_requests()
        for request in requests:
            if request.has_exceeded_the_time_limit():
                activity = request.activity
                if activity.has_min_participants():
                    has_groupe, new_data = self.create_groupe(activity)
                    if has_groupe:
                        data_to_send.append(new_data)
                else:
                    request.update_state(Request.REFUSED)
                    targets = [request.client.uid]
                    not_found_message = json_encode({"type": "not_found", "activity_type": activity.name})
                    data_to_send.append({
                        "targets": targets,
                        "message": not_found_message
                    })
        if len(data_to_send) > 0:
            callback(data_to_send)

    def test(self) -> bool:
        for table in self.tables:
            if not table.test_connection():
                return False
        return True
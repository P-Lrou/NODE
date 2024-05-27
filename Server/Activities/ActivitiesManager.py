# TOOLS
from tools.DLog import DLog
from tools.JSONTools import *
# MODEL
from Model.BaseModel import BaseModel
from Model.Activity import Activity
from Model.Member import Member
from Model.Request import Request
from Model.Room import Room
from Model.Participant import Participant

class ActivitiesManager:
    def __init__(self):
        self.tables: list[BaseModel] = [
            Activity,
            Member,
            Request,
            Room,
            Participant
        ]
        self.tables_to_reset: list[BaseModel] = [
            Request,
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
            attempting_members = activity.get_attempting_members()
            for attempting_member in attempting_members:
                request = attempting_member.get_attempting_request_by_activity(activity)
                if request:
                    request.update_state(Request.ACCEPTED)
                    participant: Participant = Participant.insert(attempting_member, room)
                    if participant:
                        targets = [attempting_member.uid for attempting_member in attempting_members]
                        new_groupe = json_encode({"type": "found", "activity_type": activity.name, "rdv_at": str(room.get_rdv_time())})
                    else:
                        DLog.LogError(f"Error to insert a participant. Member id: {attempting_member}, Room id: {room}")
                        return False, {}
                else:
                    DLog.LogError(f"Request of activity member not found. Member id: {attempting_member}, Activity: {activity.name}")
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
    def looking_for_groupe(cls, member: Member) -> tuple[bool, dict]:
        requests = member.get_requests()
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
                    member: Member = Member.get_first_member_by_uid(data["client_uid"])
                    if member:
                        request = Request.insert("", activity, member)
                        if request:
                            request_message = json_encode({"type": "new_request", "activity_type": activity_type})
                            data_to_send.append({
                                "targets": "all",
                                "message": request_message
                            })
                            DLog.LogWhisper(f"New request: {activity_type}")
                            if "is_last" in data and data["is_last"] is True:
                                has_groupe, new_data = cls.looking_for_groupe(member)
                                if has_groupe:
                                    data_to_send.append(new_data)
                            return data_to_send
                        else:
                            message_error = "Error to insert a request"
                    else:
                        message_error = f"No member found with uid: {data['client_uid']}"
                else:
                    message_error = f"No {data['activity_type']} activity found"
            else:
                message_error = "No 'client_uid' key in data"
        else:
            message_error = "No 'activity_type' in data"
        
        if not message_error:
            message_error = "THERE IS A BIG ERROR"
        data_to_send.append({
            "targets": [data["client_id"]],
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
                    member: Member = Member.get_first_member_by_uid(data["client_uid"])
                    if member:
                        request = member.get_attempting_request_by_activity(activity)
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
                            message_error = f"Request of activity member not found. Member id: {member}, Activity: {activity.name}"
                    else:
                        message_error = f"No member found. Member id: {member}"
                else:
                    message_error = f"No {data['activity_type']} activity found"
            else:
                message_error = "No 'client_uid' key in data"
        else:
            message_error = "No 'activity_type' in data"
        
        if not message_error:
            message_error = "THERE IS A BIG ERROR"
        data_to_send.append({
            "targets": [data["client_id"]],
            "message": message_error
        })
        DLog.LogError(message_error)
        return data_to_send

    @staticmethod
    def cancel_by_disconnection(client):
        member: Member = Member.get_first_member_by_uid(client["uid"])
        if member:
            requests = member.get_attempting_requests()
            for request in requests:
                request.update_state(Request.REFUSED)
            DLog.LogWhisper("Disconnection of a member, REFUSED all of his requests")
        else:
            DLog.LogError(f"No member found. uid: {client['uid']}")

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
                    targets = [request.member.uid]
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
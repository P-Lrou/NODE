# TOOLS
from tools.DLog import DLog
from tools.JSONManager import *
# MODEL
from Model.Activity import Activity
from Model.Room import Room
from Model.Participant import Participant

class ActivitiesManager:
    def __init__(self):
        Room.truncate_table()
        Participant.truncate_table()

    @staticmethod
    def new_participant(data: dict) -> list[dict]:
        data_to_send: list[dict] = []
        if "activity_type" in data: 
            activity_type = data["activity_type"]
            if "client_uid" in data: 
                activity: Activity = Activity.get_activity_by_name(activity_type)
                if activity:
                    room: Room = activity.get_first_opened_room()
                    if not room:
                        # Create room
                        room: Room = Room.insert_room(activity)
                        creation_message = json_encode({"type": "activity_created", "activity_type": activity_type})
                        data_to_send.append({
                            "targets": "all",
                            "message": creation_message
                        })
                        DLog.LogWhisper(f"New activity: {activity_type} => sending: {creation_message}")
                    
                    if room:
                        # Create participant
                        new_participant: Participant = Participant.insert_participant(data["client_id"], data["client_uid"], room)
                        if new_participant:

                            # Send data for number of participant
                            participants: list[Participant] = room.get_participants()
                            participants_count: int = len(participants)
                            new_participant_message: str = json_encode({"type": "new_participant", "activity_type": activity_type, "count": participants_count})
                            targets: list = [participant.ws_client_id for participant in participants]
                            data_to_send.append({
                                "targets": targets,
                                "message": new_participant_message
                            })
                            DLog.LogWhisper(f"New participant to {activity_type} => sending: {new_participant_message}")

                            # If the activity is full
                            if participants_count >= room.activity.max_participants:
                                room.close()
                                complete_message = json_encode({"type": "activity_full", "activity_type": activity_type})
                                data_to_send.append({
                                    "target": targets,
                                    "message": complete_message
                                })
                                DLog.LogWhisper(f"Activity {activity_type} is full => sending: {complete_message}")

                            return data_to_send
                        else:
                            message_error = "Can't add participant to the activity"
                    else:
                        message_error = "Error to find a valid room"
                else:
                    message_error = f"No {data["activity_type"]} activity found"
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
    def drop_participant_by_activity(data: dict) -> list[dict]:
        data_to_send: list[dict] = []
        if "activity_type" in data:
            activity_type = data["activity_type"]
            if "client_uid" in data:
                activity: Activity = Activity.get_activity_by_name(activity_type)
                if activity:
                    room: Room = activity.get_first_opened_room()
                    if room:
                        # Delete participant with good uid
                        participants_to_drop: list[Participant] = Participant.get_participants_by_room_and_uid(room, data["client_uid"])
                        if len(participants_to_drop) > 0:
                            participant_to_drop = participants_to_drop[0]
                            Participant.delete_by_id(participant_to_drop)
                            leave_message = json_encode({"type": "activity_leave", "activity_type": activity_type})
                            data_to_send.append({
                                "targets": [data["client_id"]],
                                "message": leave_message
                            })
                            DLog.LogWhisper(f"A participant leave the activity {activity_type} => sending: {leave_message}")

                            # Send data for number of participant
                            participants: list[Participant] = room.get_participants()
                            participants_count = len(participants)
                            # If room is empty
                            if participants_count <= 0:
                                empty_message = json_encode({"type": "activity_empty", "activity_type": activity_type})
                                data_to_send.append({
                                    "targets": "all",
                                    "message": empty_message
                                })
                                DLog.LogWhisper(f"Activity {activity_type} is empty => sending: {empty_message}")
                                Room.delete_by_id(room)
                            else:
                                drop_participant_message = json_encode({"type": "drop_participant", "activity_type": activity_type, "count": participants_count})
                                targets :list = [participant.ws_client_id for participant in participants]
                                data_to_send.append({
                                    "targets": targets,
                                    "message": drop_participant_message
                                })
                                DLog.LogWhisper(f"Drop participant to {activity_type} => sending: {drop_participant_message}")
                            return data_to_send
                        else:
                            message_error = f"Participant not found in the opnened room of {activity_type} activity. uid: {data['uid']}"
                    else:
                        message_error = "Error to find a valid room"
                else:
                    message_error = f"No {data["activity_type"]} activity found"
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
    def drop_participant_by_client(client) -> list[dict]:
        data_to_send: list[dict] = []
        participants_to_drop: list[Participant] = Participant.get_participants_by_uid(client["uid"])
        for participant in participants_to_drop:
            room: Room = participant.room
            activity_type = room.activity.name
            if not room.is_opened():
                continue
            Participant.delete_by_id(participant)
            participants: list[Participant] = room.get_participants()
            participants_count = len(participants)
            # If room is empty
            if participants_count <= 0:
                empty_message = json_encode({"type": "activity_empty", "activity_type": activity_type})
                data_to_send.append({
                    "targets": "all",
                    "message": empty_message
                })
                DLog.LogWhisper(f"Activity {activity_type} is empty => sending: {empty_message}")
                Room.delete_by_id(room)
            else:
                drop_participant_message = json_encode({"type": "drop_participant", "activity_type": activity_type, "count": participants_count})
                targets: list = [participant.ws_client_id for participant in participants]
                data_to_send.append({
                    "targets": targets,
                    "message": drop_participant_message
                })
                DLog.LogWhisper(f"Drop participant to {activity_type} => sending: {drop_participant_message}")
        if len(data_to_send) > 0:
            return data_to_send
        
        message_error = "No participant to drop found"
        data_to_send.append({
            "targets": [client["id"]],
            "message": message_error
        })
        DLog.LogError(message_error)
        return data_to_send

    @staticmethod
    def check_room_waiting_time(callback):
        data_to_send: list[dict] = []
        rooms: list[Room] = Room.get_opened_rooms()
        for room in rooms:
            if room.is_finished_to_wait():
                activity_type = room.activity.name
                participants: list[Participant] = room.get_participants()
                room.close()
                complete_message = json_encode({"type": "activity_full", "activity_type": activity_type})
                data_to_send.append({
                    "target": [participant.ws_client_id for participant in participants],
                    "message": complete_message
                })
                DLog.LogWhisper(f"Activity {activity_type} is full => sending: {complete_message}")
        if len(data_to_send) > 0:
            callback(data_to_send)
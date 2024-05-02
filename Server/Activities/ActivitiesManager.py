import json
from tools.DLog import DLog
from Model.Activity import Activity
from Model.Room import Room
from Model.Participant import Participant

class ActivitiesManager:
    def __init__(self):
        Room.truncate_table()
        Participant.truncate_table()
        pass
    
    def add_participant(self, room_id, client):
        room = Room.get_or_none(Room.id == room_id)
        if room:
            if Participant.insert_participant(client["id"], client["uid"], room):
                return True
            else:
                DLog.LogError("Error when inserting participant")
        else:
            DLog.LogError(f"Room not found")
        return False
    
    def remove_participant(self, activity_type, client):
        activity = Activity.get_activity_by_name(activity_type)
        if activity:
            participants = activity.get_participants()
            if len(participants) > 0:
                for participant in participants:
                    if participant.uid == client["uid"]:
                        Participant.delete_by_id(participant)
                return True
            else:
                DLog.LogError(f"Any participant with this uid has found in '{activity_type} activity")
        else:
            DLog.LogError(f"Activity '{activity_type}' not found")
        return False

    def get_participants(self, room_id):
        room = Room.get_or_none(Room.id == room_id)
        if room:
            return room.get_participants()
        else:
            return []
    
    def open_new_room(self, activity_type):
        activity = Activity.get_activity_by_name(activity_type)
        if activity:
            return Room.insert_room(activity)
        else:
            return None
    
    def get_opened_room(self, activity_type):
        activity = Activity.get_activity_by_name(activity_type)
        if activity:
            rooms = activity.get_opened_rooms()
            if len(rooms) > 0:
                return rooms[0]
            else:
                return None
        else:
            DLog.LogError(f"Activity {activity_type} not found")
        return None
    
    def delete_room(self, room_id):
        room = Room.get_or_none(Room.id == room_id)
        if room:
            Room.delete_by_id(room)
            return True
        else:
            DLog.LogError("Room not found")
        return False
            

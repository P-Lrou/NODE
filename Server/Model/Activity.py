from tools.DLog import DLog
from Model.BaseModel import *

class Activity(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()
    min_participants = IntegerField(default=2)
    max_participants = IntegerField(default=6)
    max_seconds_waiting_time = IntegerField(default=900)

    class Meta:
        table_name = 'activities'

    @classmethod
    def get_activity_by_name(cls, name):
        if name:
            return cls.get_or_none(cls.name == name)
        else:
            DLog.LogError("Name is required")
            return None
        
    def get_rooms(self) ->list:
        from Model.Room import Room
        return (Room
                .select()
                .where(Room.activity == self))
    
    def get_participants(self) -> list:
        from Model.Room import Room
        from Model.Participant import Participant
        return (Participant
                .select()
                .join(Room)
                .where(
                    (Room.activity == self) &
                    (Participant.room == Room.id)
                ))

    def get_opened_rooms(self) -> list:
        from Model.Room import Room
        from Model.Participant import Participant
        rooms = (Room
                 .select()
                 .where(
                     (Room.activity_id == self) &
                     (Room.opened == 1)
                ))
        return rooms
    
    def get_first_opened_room(self):
        rooms = self.get_opened_rooms()
        if len(rooms) > 0:
            return rooms[0]
        else:
            return None
    
    def has_min_participants(self) -> bool:
        return len(self.get_participants()) >= self.min_participants
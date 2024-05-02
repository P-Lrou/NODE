from tools.DLog import DLog
from Model.BaseModel import *

class Activity(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()
    required_participants = IntegerField(default=2)

    class Meta:
        table_name = 'activities'

    @classmethod
    def insert_activity(cls, name, required_participants=2):
        if name:
            return cls.create(name=name, required_participants=required_participants)
        else:
            DLog.LogError("Name is required")
            return None

    @classmethod
    def get_activity_by_name(cls, name):
        if name:
            return cls.get_or_none(cls.name == name)
        else:
            DLog.LogError("Name is required")
            return None
        
    def get_rooms(self):
        from Model.Room import Room
        return (Room
                .select()
                .where(Room.activity == self))
    
    def get_participants(self):
        from Model.Room import Room
        from Model.Participant import Participant
        return (Participant
                .select()
                .join(Room)
                .where(
                    (Room.activity == self) &
                    (Participant.room == Room.id)
                ))

    def get_opened_rooms(self):
        from Model.Room import Room
        from Model.Participant import Participant
        rooms = (Room
                 .select()
                 .join(Participant, JOIN.LEFT_OUTER)  # Assurez-vous de capturer les chambres même sans participants
                 .where(Room.activity_id == self)
                 .group_by(Room.id)
                 .having(fn.COUNT(Participant.id) < self.required_participants))
        return rooms
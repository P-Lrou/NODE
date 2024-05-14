from tools.DLog import DLog
from Model.BaseModel import *

class Room(BaseModel):
    from Model.Activity import Activity
    id = IntegerField(primary_key=True)
    activity = ForeignKeyField(Activity, backref='rooms')

    class Meta:
        table_name = 'rooms'

    @classmethod
    def insert_room(cls, activity):
        return cls.create(activity=activity)

    @classmethod
    def get_rooms_by_activity(cls, activity):
        return cls.select().where(cls.activity == activity)
    
    def get_participants(self):
        from Model.Participant import Participant
        return (Participant
                .select()
                .where(Participant.room == self))
    
    def is_opened(self):
        opened_rooms = self.activity.get_opened_rooms()
        if len(opened_rooms) > 0:
            return self in opened_rooms
        else:
            return False
        

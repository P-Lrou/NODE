from tools.DLog import DLog
from Model.BaseModel import *
import datetime

class Room(BaseModel):
    from Model.Activity import Activity
    id = IntegerField(primary_key=True)
    activity:Activity = ForeignKeyField(Activity, backref='rooms')
    opened = IntegerField()
    created_at = DateTimeField()

    class Meta:
        table_name = 'rooms'

    @classmethod
    def insert_room(cls, activity):
        return cls.create(activity=activity, opened=1, created_at=datetime.datetime.now())

    @classmethod
    def get_rooms_by_activity(cls, activity) -> list:
        return cls.select().where(cls.activity == activity)
    
    @classmethod
    def get_opened_rooms(cls) -> list:
        return cls.select().where(cls.opened == 1)
    
    def get_participants(self) -> list:
        from Model.Participant import Participant
        return (Participant
                .select()
                .where(Participant.room == self))
    
    def is_opened(self) -> bool:
        return self.opened == 1
    
    def is_finished_to_wait(self) -> bool:
        actual_datetime = datetime.datetime.now()
        duration = self.created_at - actual_datetime
        return duration.total_seconds() >= self.activity.max_seconds_waiting_time
    
    def close(self) -> None:
        self.opened = 0
        self.save()
        

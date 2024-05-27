from tools.DLog import DLog
from Model.BaseModel import *
from typing import List, Optional, TYPE_CHECKING
import datetime

if TYPE_CHECKING:
    from Model.Activity import Activity
    from Model.Participant import Participant

class Room(BaseModel):
    from Model.Activity import Activity
    backref = "rooms"
    id = IntegerField(primary_key=True)
    activity: Activity = ForeignKeyField(Activity, backref=backref)
    created_at = DateTimeField()

    DELTA_MINUTES = 30
    DIFF_TIMEZONE = 2

    class Meta:
        table_name = 'rooms'

    @classmethod
    def insert(cls, activity: "Activity", **insert) -> "Room":
        data = {
            "activity": activity,
            "created_at": datetime.datetime.now() + datetime.timedelta(hours=cls.DIFF_TIMEZONE)
        }
        query: ModelInsert = super(Room, cls).insert(data, **insert)
        room_id = query.execute()
        room = cls.get_by_id(room_id)
        return room
    
    def get_participants(self) -> List["Participant"]:
        return list(self.participants)
    
    def get_rdv_time(self):
        rdv_time: datetime.datetime = self.created_at + datetime.timedelta(minutes=self.DELTA_MINUTES)
        return rdv_time.strftime("%H:%M")
        

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

    class Meta:
        table_name = 'rooms'

    @classmethod
    def insert(cls, activity: "Activity", **insert) -> "Room":
        data = {
            "activity": activity,
            "created_at": datetime.datetime.now()
        }
        query: ModelInsert = super(Room, cls).insert(data, **insert)
        room = query.execute()
        return room
    
    def get_participants(self) -> List["Participant"]:
        return list(self.participants)
        

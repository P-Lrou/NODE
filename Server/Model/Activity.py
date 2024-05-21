from tools.DLog import DLog
from Model.BaseModel import *
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from Model.Request import Request
    from Model.Member import Member
    from Model.Room import Room

class Activity(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()
    min_participants = IntegerField(default=2)
    max_participants = IntegerField(default=6)
    max_duration = IntegerField(default=900)

    class Meta:
        table_name = 'activities'

    @classmethod
    def get_activity_by_name(cls, name: str) -> Optional["Activity"]:
        if name:
            return cls.get_or_none(cls.name == name)
        else:
            DLog.LogError("Name is required")
            return None
    
    def get_requests(self) -> List["Request"]:
        return list(self.requests)
    
    def get_attempting_requests(self) -> List["Request"]:
        from Model.Request import Request
        return [request for request in self.requests if request.state == Request.ATTEMPTING]
    
    def get_attempting_members(self) -> List["Member"]:
        attempting_requests = self.get_attempting_requests()
        return [request.member for request in attempting_requests]
    
    def has_min_participants(self) -> bool:
        return len(self.get_attempting_members()) >= self.min_participants
    
    def get_rooms(self) -> List["Room"]:
        return list(self.rooms)
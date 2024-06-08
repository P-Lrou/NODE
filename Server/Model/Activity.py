from tools.DLog import DLog
from Model.BaseModel import *
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from Model.Request import Request
    from Model.Client import Client
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
        return cls.get_or_none(cls.name == name)

    @classmethod
    def get_activities_by_names(cls, names: list[str]) -> List["Activity"]:
        if not names:
            return []
        return list(cls.select().where(cls.name.in_(names)))
    
    def get_requests(self) -> List["Request"]:
        return list(self.requests)
    
    def get_attempting_requests(self) -> List["Request"]:
        from Model.Request import Request
        return [request for request in self.requests if request.state == Request.ATTEMPTING]
    
    def get_attempting_clients(self) -> List["Client"]:
        attempting_requests = self.get_attempting_requests()
        return [request.client for request in attempting_requests]
    
    def has_min_participants(self) -> bool:
        return len(self.get_attempting_clients()) >= self.min_participants
    
    def has_max_participants(self) -> bool:
        return len(self.get_attempting_clients()) == self.max_participants
    
    def get_rooms(self) -> List["Room"]:
        return list(self.rooms)
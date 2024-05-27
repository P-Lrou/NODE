from tools.DLog import DLog
from Model.BaseModel import *
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from Model.Activity import Activity
    from Model.Request import Request

class Member(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()
    uid = CharField()

    class Meta:
        table_name = 'members'

    @classmethod
    def insert(cls, name: str, uid: str, **insert) -> "Member":
        data = {
            'name': name,
            'uid': uid
        }
        query: ModelInsert = super(Member, cls).insert(data, **insert)
        member_id = query.execute()
        member = cls.get_by_id(member_id)
        return member
    
    @classmethod
    def get_members_by_name(cls, name: str) -> List["Member"]:
        return list(cls.select().where(cls.name == name))
    
    @classmethod
    def get_first_member_by_name(cls, name: str) -> Optional["Member"]:
        members = cls.get_members_by_name(name)
        return members[0] if members else None
    
    @classmethod
    def get_last_member_by_name(cls, name: str) -> Optional["Member"]:
        members = cls.get_members_by_name(name)
        return members[-1] if members else None
    
    @classmethod
    def get_members_by_uid(cls, uid: str) -> List["Member"]:
        return list(cls.select().where(cls.uid == uid))

    @classmethod
    def get_first_member_by_uid(cls, uid: str) -> Optional["Member"]:
        members = cls.get_members_by_uid(uid)
        return members[0] if members else None
    
    def get_requests(self) -> List["Request"]:
        return [request for request in self.requests]
    
    def get_attempting_requests(self) -> List["Request"]:
        from Model.Request import Request
        return [request for request in self.requests if request.state == Request.ATTEMPTING]
    
    def get_attempting_request_by_activity(self, activity: "Activity") -> Optional["Request"]:
        from Model.Request import Request
        requests = [request for request in self.requests if request.state == Request.ATTEMPTING and request.activity == activity]
        if requests:
            return requests[0]
        else:
            return None

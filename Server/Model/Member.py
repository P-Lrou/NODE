from tools.DLog import DLog
from Model.BaseModel import *
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
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
        member = query.execute()
        return member
    
    @classmethod
    def get_members_by_name(cls, name: str) -> Optional["Member"]:
        query = cls.select().where(cls.name == name)
        members = cls.query_to_list(query)
        return members
    
    @classmethod
    def get_first_member_by_name(cls, name: str) -> Optional["Member"]:
        members = cls.get_members_by_name(name)
        return members[0] if members else None
    
    @classmethod
    def get_last_member_by_name(cls, name: str) -> Optional["Member"]:
        members = cls.get_members_by_name(name)
        return members[-1] if members else None
    
    def get_requests(self) -> List["Request"]:
        return [request for request in self.requests]
    
    def get_attempting_requests(self) -> List["Request"]:
        from Model.Request import Request
        return [request for request in self.requests if request.state == Request.ATTEMPTING]
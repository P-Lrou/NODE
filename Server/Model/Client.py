from tools.DLog import DLog
from Model.BaseModel import *
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from Model.Activity import Activity
    from Model.Request import Request
    from Model.Contact import Contact

class Client(BaseModel):
    backref = "clients"
    from Model.Contact import Contact
    id = IntegerField(primary_key=True)
    uid = CharField()
    contact: Contact = ForeignKeyField(Contact, backref=backref)

    class Meta:
        table_name = 'clients'

    @classmethod
    def insert(cls, uid: str, contact: "Contact" = None, **insert) -> "Client":
        data = {
            'uid': uid,
            "contact": contact
        }
        query: ModelInsert = super(Client, cls).insert(data, **insert)
        client_id = query.execute()
        client = cls.get_by_id(client_id)
        return client
    
    @classmethod
    def get_clients_by_uid(cls, uid: str) -> List["Client"]:
        return list(cls.select().where(cls.uid == uid))

    @classmethod
    def get_first_client_by_uid(cls, uid: str) -> Optional["Client"]:
        clients = cls.get_clients_by_uid(uid)
        return clients[0] if clients else None
    
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
        
    def update_contact(self, contact):
        self.contact = contact
        self.save()
        return True

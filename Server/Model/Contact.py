from tools.DLog import DLog
from Model.BaseModel import *
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from Model.Activity import Activity
    from Model.Request import Request

class Contact(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()

    class Meta:
        table_name = 'contacts'

    @classmethod
    def insert(cls, name: str, **insert) -> "Contact":
        data = {
            'name': name
        }
        query: ModelInsert = super(Contact, cls).insert(data, **insert)
        contact_id = query.execute()
        contact = cls.get_by_id(contact_id)
        return contact
    
    @classmethod
    def get_contact_by_name(cls, name: str) -> "Contact":
        contacts: list[Contact] = list(cls.select().where(cls.name == name))
        return contacts[0]

from tools.DLog import DLog
from Model.BaseModel import *
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from Model.Room import Room
    from Model.Client import Client

class Participant(BaseModel):
    from Model.Room import Room
    from Model.Client import Client
    backref = "participants"
    id = IntegerField(primary_key=True)
    client: Client = ForeignKeyField(Client, backref=backref)
    room: Room = ForeignKeyField(Room, backref=backref)

    class Meta:
        table_name = 'participants'

    @classmethod
    def insert(cls, client: "Client", room: "Room", **insert) -> "Participant":
        data = {
            "client": client,
            "room": room
        }
        query: ModelInsert = super(Participant, cls).insert(data, **insert)
        participant_id = query.execute()
        participant = cls.get_by_id(participant_id)
        return participant

        
    
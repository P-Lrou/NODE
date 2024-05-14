from tools.DLog import DLog
from Model.BaseModel import *

class Participant(BaseModel):
    from Model.Room import Room
    id = IntegerField(primary_key=True)
    ws_client_id = IntegerField()
    uid = CharField()
    room = ForeignKeyField(Room, backref='participants')

    class Meta:
        table_name = 'participants'

    @classmethod
    def insert_participant(cls, ws_client_id, uid, room):
        if ws_client_id:
            if uid:
                return cls.create(ws_client_id=ws_client_id, uid=uid, room=room)
            else:
                DLog.LogError("UID is require")
        else:
            DLog.LogError("Websocket client ID is require")
        return None

    @classmethod
    def get_participants_by_uid(cls, uid):
        if uid:
            return cls.select().where(cls.uid == uid)
        else:
            DLog.LogError("UID is require")
            return []
    
    @classmethod
    def get_participants_by_ws_client_id(cls, ws_client_id):
        if ws_client_id:
            return cls.select().where(cls.ws_client_id == ws_client_id)
        else:
            DLog.LogError("Websocket client ID is require")
            return None
        
    
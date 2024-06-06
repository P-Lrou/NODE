from tools.DLog import DLog
from Model.BaseModel import *
from typing import List, Optional, TYPE_CHECKING
import datetime

if TYPE_CHECKING:
    from Model.Activity import Activity
    from Model.Client import Client

class Request(BaseModel):
    from Model.Activity import Activity
    from Model.Client import Client
    backref = "requests"
    id = IntegerField(primary_key=True)
    state = CharField()
    activity: Activity = ForeignKeyField(Activity, backref=backref)
    client: Client = ForeignKeyField(Client, backref=backref)
    created_at = DateTimeField()

    ACCEPTED = "accepted"
    REFUSED = "refused"
    ATTEMPTING = "attempting"
    DISCONNECTED = "disconnected"

    state_possibilities = [
        ACCEPTED,
        REFUSED,
        ATTEMPTING
    ]

    class Meta:
        table_name = 'requests'

    @classmethod
    def __check_state_value(cls, state):
        if state == "":
            state = cls.ATTEMPTING
        if state not in cls.state_possibilities:
            DLog.LogError(f"'state' does not contain a valid value")
            return cls.ATTEMPTING
        return state

    @classmethod
    def insert(cls, state: str, activity: "Activity", client: "Client", **insert) -> "Request":
        state = cls.__check_state_value(state)
        data = {
            "state": state,
            "activity": activity,
            "client": client,
            "created_at": datetime.datetime.now()
        }
        query: ModelInsert = super(Request, cls).insert(data, **insert)
        request_id = query.execute()
        request = cls.get_by_id(request_id)
        return request

    @classmethod
    def get_attempting_requests(cls) -> List["Request"]:
        return list(cls.select().where(Request.state == Request.ATTEMPTING))

    def update_state(self, state: str) -> bool:
        if not Request.__check_state_value(state):
            return False
        self.state = state
        self.save()
        return True

    def has_exceeded_the_time_limit(self) -> bool:
        actual_time = datetime.datetime.now()
        timedelta = datetime.timedelta(seconds=self.activity.max_duration)
        return actual_time > (self.created_at + timedelta)

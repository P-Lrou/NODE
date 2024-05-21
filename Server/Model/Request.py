from tools.DLog import DLog
from Model.BaseModel import *
from typing import List, Optional, TYPE_CHECKING
import datetime

if TYPE_CHECKING:
    from Model.Activity import Activity
    from Model.Member import Member

class Request(BaseModel):
    from Model.Activity import Activity
    from Model.Member import Member
    backref = "requests"
    id = IntegerField(primary_key=True)
    state = CharField()
    activity: Activity = ForeignKeyField(Activity, backref=backref)
    member: Member = ForeignKeyField(Member, backref=backref)
    created_at = DateTimeField()

    ACCEPTED = "accepted"
    REFUSED = "refused"
    ATTEMPTING = "attempting"

    state_possibilities = [
        ACCEPTED,
        REFUSED,
        ATTEMPTING
    ]

    class Meta:
        table_name = 'requests'

    @classmethod
    def __check_state_value(cls, state):
        if state not in cls.state_possibilities:
            DLog.LogError(f"'state' does not contain a valid value")
            return False
        return True

    @classmethod
    def insert(cls, state: str, activity: "Activity", member: "Member", **insert) -> "Request":
        if not cls.__check_state_value(state):
            return None
        data = {
            "state": state,
            "activity": activity,
            "member": member,
            "created_at": datetime.datetime.now()
        }
        query: ModelInsert = super(Request, cls).insert(data, **insert)
        request = query.execute()
        return request

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

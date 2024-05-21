from Model.Activity import Activity
from Model.Member import Member
from Model.Request import Request
from Model.Room import Room
from Model.Participant import Participant

activity = Activity.get_activity_by_name("belote")

# member = Member.insert("michel", "qsjgfisgjhqg")
member = Member.get_last_member_by_name("michel")

# request = Request.insert(Request.ATTEMPTING, activity, member)
# requests = activity.get_attempting_requests()
# for request in requests:
#     if request.has_exceeded_the_time_limit():
#         request.update_state(Request.REFUSED)

# room = Room.insert(activity)
room = activity.get_rooms()[0]
# participant = Participant.insert(member, room)
participant = room.get_participants()[0]
print(participant.member.name)
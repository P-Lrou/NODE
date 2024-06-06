from Model.Activity import Activity
from Model.Client import Client
from Model.Request import Request
from Model.Room import Room
from Model.Participant import Participant

activity = Activity.get_activity_by_name("belote")

# client = Client.insert("michel", "qsjgfisgjhqg")
client = Client.get_last_client_by_name("michel")

# request = Request.insert(Request.ATTEMPTING, activity, client)
# requests = activity.get_attempting_requests()
# for request in requests:
#     if request.has_exceeded_the_time_limit():
#         request.update_state(Request.REFUSED)

Room.truncate_table()
room = Room.insert(activity)
# participant = Participant.insert(client, room)
# participant = room.get_participants()[0]
print(room.get_rdv_time())
from tools.DLog import DLog
from Activities.ActivitiesManager import ActivitiesManager

class ClientHandler:
    def __init__(self) -> None:
        pass

    def process_message(self, data:dict) -> dict:
        if "client_id" in data:
            if "type" in data:
                type = data["type"] 
                if type == "activity":
                    if "state" in data:
                        state = data["state"]
                        match state:
                            case "joined":
                                return ActivitiesManager.new_participant(data)
                            case "retired":
                                return ActivitiesManager.drop_participant_by_activity(data)
                            case _:
                                message_error = f"Unknown state: {state}"
                    else:
                        message_error = "No 'state' key in data"
                else:
                    message_error = f"Unknwon type: {type}"
            else:
                message_error = "No 'type' key in data"
        else:
            message_error = "Client ID is missing"

        if not message_error:
            message_error = "THERE IS A BIG ERROR"
        DLog.LogError(message_error)
        return {'error':message_error}
            
            

    def process_disconnection(self, client) -> dict:
        return ActivitiesManager.drop_participant_by_client(client)



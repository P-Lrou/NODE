from tools.DLog import DLog


class ActivitiesManager:

    def __init__(self):
        pass

    def new_activity(self, activity):
        # for the moment we juste print the activity waiting the activites managment system
        DLog.Log(f"{activity}")

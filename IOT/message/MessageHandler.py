from GlobalVariables import *
from tools.Sound import PlaySound

class MessageHandler:
    def __init__(self) -> None:

        #* Led controller
        from led.LedController import LEDController
        self.led_matchmaking = LEDController(pin_numbers=LedPins.instance().matchmaking_number)
        self.led_activities = LEDController(pin_by_name=LedPins.instance().activities_led_number)

    def process_message(self, json_message):
        if "type" in json_message:
            if json_message["type"] == "activity_created":
                activity_type = json_message["activity_type"]
                self.led_activities.on_name(activity_type)
            elif json_message["type"] == "new_participant":
                last_number_participant = self.led_matchmaking.counter
                actual_number_participant = json_message["count"]
                loop_number = abs(actual_number_participant - last_number_participant)
                if actual_number_participant > last_number_participant:
                    PlaySound.join()
                    for i in range(0, loop_number):
                        self.led_matchmaking.on_next()
                else:
                    DLog.LogWarning("There is not new participant")
            elif json_message["type"] == "drop_participant":
                last_number_participant = self.led_matchmaking.counter
                actual_number_participant = json_message["count"]
                loop_number = abs(actual_number_participant - last_number_participant)
                if actual_number_participant < last_number_participant:
                    PlaySound.leave()
                    for i in range(0, loop_number):
                        self.led_matchmaking.off_previous()
                else:
                    DLog.LogWarning("There is not drop participant")
            elif json_message["type"] == "activity_leave":
                PlaySound.leave()
                self.led_matchmaking.all_off()
            elif json_message["type"] == "activity_full":
                activity_type = json_message["activity_type"]
                DLog.LogSuccess(f"Printing of {activity_type} result...")
                PlaySound.print()
                self.led_matchmaking.blinking()
            elif json_message["type"] == "activity_empty":
                PlaySound.leave()
                activity_type = json_message["activity_type"]
                self.led_activities.off_name(activity_type)
            else:
                PlaySound.error()
                DLog.LogError("Unknown type")
        elif "uid" in json_message:
            DLog.LogWarning("Nothing to do with uid")
        else:
            DLog.LogError("Can't treat this message")



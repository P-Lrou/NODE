from GlobalVariables import *

class MessageHandler:
    def __init__(self) -> None:

        #* Led controller
        from led.LedController import LEDController
        self.led_matchmaking = LEDController(pin_numbers=LedPins.instance().matchmaking_number)
        self.led_activities = LEDController(pin_by_name=LedPins.instance().activities_led_number)

    def process_message(self, json_message):
        if "type" in json_message:
            if json_message["type"] == "activity_created":
                activity = json_message["activity_type"]
                self.led_activities.on_name(activity)
            elif json_message["type"] == "new_participant":
                last_number_participant = self.led_matchmaking.counter
                actual_number_participant = json_message["count"]
                loop_number = abs(last_number_participant - actual_number_participant)
                print(loop_number)
                if actual_number_participant > last_number_participant:
                    for i in range(0, loop_number):
                        self.led_matchmaking.on_next()
                elif actual_number_participant < last_number_participant:
                    for i in range(0, loop_number):
                        self.led_matchmaking.off_next()
                else:
                    print("Good participant number")
            elif json_message["type"] == "activity_full":
                activity = json_message["activity_type"]
                print(f"Printing of {activity} result...")
                self.led_matchmaking.clignotment()
            else:
                print("Error: Unknown type")
        else:
            print("Error: Can't treat this message")



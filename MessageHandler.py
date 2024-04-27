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
                self.led_activities.on(activity)
            elif json_message["type"] == "new_participant":
                last_number_participant = self.led_matchmaking.counter
                actual_number_participant = json_message["count"]
                loop_number = abs(last_number_participant - actual_number_participant)
                if actual_number_participant > last_number_participant:
                    for i in range(1, loop_number):
                        self.led_matchmaking.on()
                elif actual_number_participant < last_number_participant:
                    for i in range(1, loop_number):
                        self.led_matchmaking.off()
                else:
                    print("Good participant number")
            elif json_message["type"] == "activity_full":
                activity = json_message["activity_type"]
                print(f"Printing of {activity} result...")
            else:
                print("Error: Unknown type")
        else:
            print("Error: Can't treat this message")



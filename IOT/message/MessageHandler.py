from GlobalVariables import *
from tools.Sound import PlaySound
from tools.Printer import Printer
from dock.Dock import Dock

class MessageHandler:
    def __init__(self, parent) -> None:
        self.parent = parent

    def process_message(self, json_message):
        if "type" in json_message:
            if json_message["type"] == "new_request":
                pass
            elif json_message["type"] == "join":
                # PLAY JOIN SOUND
                PlaySound.join()
                # LIGHT ON RING LED
                activity_type = json_message["activity_type"]
                if self.parent:
                    dock: Dock = self.parent.get_dock_by_activity(activity_type)
                    dock.launch_circle()
                pass
            elif json_message["type"] == "leave":
                activity_type = json_message["activity_type"]
                # PLAY LEAVE SOUND
                PlaySound.leave()
                # LIGHT OFF RING LEDS
                activity_type = json_message["activity_type"]
                if self.parent:
                    dock: Dock = self.parent.get_dock_by_activity(activity_type)
                    dock.launch_stop()
                pass
            elif json_message["type"] == "found":
                activity_type = json_message["activity_type"]
                # PLAY PRINTING SOUND
                PlaySound.print()
                # LIGHT ON RING LED
                activity_type = json_message["activity_type"]
                if self.parent:
                    dock: Dock = self.parent.get_dock_by_activity(activity_type)
                    dock.launch_success()
                    docks: list[Dock] = self.parent.get_docks_by_non_activity(activity_type)
                    for dock in docks:
                        dock.launch_stop()
                #TODO: GENERATE IMAGE
                image_path = "ressources/images/ticket_imprimante.png"
                # PRINT IMAGE
                Printer.switch_state()
                time.sleep(3)
                Printer.print(image_path)
                DLog.LogSuccess(f"Printing of {activity_type} result...")
            elif json_message["type"] == "not_found":
                #TODO: PLAY NOT_FOUND SOUND
                # BLINKING ERROR ACTIVITY LED
                activity_type = json_message["activity_type"]
                if self.parent:
                    docks: list[Dock] = self.parent.get_docks()
                    for dock in docks:
                        dock.launch_error()
                pass
            else:
                PlaySound.error()
                DLog.LogError("Unknown type")
        elif "uid" in json_message:
            pass
        else:
            DLog.LogError("Can't treat this message")



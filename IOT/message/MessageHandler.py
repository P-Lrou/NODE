from GlobalVariables import *
from tools.Timer import Timer
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
                # PLAY LEAVE SOUND
                PlaySound.leave()
                # LIGHT OFF RING LEDS
                activity_type = json_message["activity_type"]
                if self.parent:
                    dock: Dock = self.parent.get_dock_by_activity(activity_type)
                    dock.launch_circle()
                pass
            elif json_message["type"] == "found":
                # PLAY PRINTING SOUND
                PlaySound.print()
                # LIGHT ON RING LED
                activity_type = json_message["activity_type"]
                if self.parent:
                    dock: Dock = self.parent.get_dock_by_activity(activity_type)
                    dock.launch_circle()
                #TODO: GENERATE IMAGE
                image_path = "ressources/images/ticket_imprimante.png"
                # PRINT IMAGE
                Printer.print(image_path)
                DLog.LogSuccess(f"Printing of {activity_type} result...")
            elif json_message["type"] == "not_found":
                #TODO: PLAY NOT_FOUND SOUND
                # BLINKING ERROR ACTIVITY LED
                activity_type = json_message["activity_type"]
                if self.parent:
                    dock: Dock = self.parent.get_dock_by_activity(activity_type)
                    dock.launch_circle()
                pass
            else:
                PlaySound.error()
                DLog.LogError("Unknown type")
        elif "uid" in json_message:
            pass
        else:
            DLog.LogError("Can't treat this message")



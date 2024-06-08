from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from IOTManager import IOTManager
from GlobalVariables import *
from tools.Sound import PlaySound
from printer.Printer import ThermalPrinter
from led.LedManager import LEDManager

class MessageHandler:
    def __init__(self, iot_manager: "IOTManager") -> None:
        self.iot_manager = iot_manager
        self.trafic_led = LEDManager(pin_numbers=LedPins.instance().trafic_number)

    def process_message(self, json_message):
        if "type" in json_message:
            if json_message["type"] == "new_request":
                # BLINK CLASSIC LED
                self.trafic_led.all_blinking(blinking_repeat=1)
                pass
            elif json_message["type"] == "join":
                activity_type = json_message["activity_type"]
                # LIGHT ON RING LED
                self.iot_manager.dock_manager.activity_join(activity_type)
            elif json_message["type"] == "leave":
                activity_type = json_message["activity_type"]
                # LIGHT OFF RING LEDS
                self.iot_manager.dock_manager.activity_leave(activity_type)
            elif json_message["type"] == "found":
                activity_type = json_message["activity_type"]
                # PLAY PRINTING SOUND
                PlaySound.print()
                activity_type = json_message["activity_type"]
                # LIGHT ON FOUND RING LED
                self.iot_manager.dock_manager.activity_found(activity_type)
                #TODO: GENERATE IMAGE
                image_path = "ressources/images/ticket_imprimante.png"
                # PRINT IMAGE
                ThermalPrinter.switch_state()
                time.sleep(3)
                ThermalPrinter.print(image_path)
                ThermalPrinter.switch_state()
                DLog.LogSuccess(f"Printing of {activity_type} result...")
            elif json_message["type"] == "not_found":
                activity_type = json_message["activity_type"]
                # LIGHT ON NOT FOUND RING LED
                self.iot_manager.dock_manager.activity_not_found(activity_type)
            else:
                PlaySound.error()
                DLog.LogError("Unknown type")
        elif "uid" in json_message:
            pass
        else:
            DLog.LogError("Can't treat this message")



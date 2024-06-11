from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from IOTManager import IOTManager
from GlobalVariables import *
from tools.Sound import PlaySound
from printer.Printer import ThermalPrinter
from printer.Ticket import Ticket
from led.LedManager import LEDManager

class MessageHandler:
    def __init__(self, iot_manager: "IOTManager") -> None:
        self.iot_manager = iot_manager
        self.trafic_led = LEDManager(pin_numbers=LedPins.instance().trafic_number)
        self.printer = ThermalPrinter()

    def process_message(self, json_message):
        if "type" in json_message:
            if json_message["type"] == "new_request":
                # SWITCH ON ONE CLASSIC LED
                self.trafic_led.all_on()
            elif json_message["type"] == "no_attempting":
                # SWITCH OFF ONE CLASSIC LED
                self.trafic_led.all_off()
            elif json_message["type"] == "search":
                activity_type = json_message["activity_type"]
                # LIGHT ON RING LED
                self.iot_manager.dock_manager.activity_search(activity_type)
            elif json_message["type"] == "cancel":
                activity_type = json_message["activity_type"]
                # LIGHT OFF RING LEDS
                self.iot_manager.dock_manager.activity_cancel(activity_type)
            elif json_message["type"] == "found":
                activity_type = json_message["activity_type"]
                # LIGHT ON FOUND RING LED
                self.iot_manager.dock_manager.activity_found(activity_type)
                # PLAY PRINTING SOUND
                PlaySound.print()
                # GENERATE IMAGE
                ticket = Ticket.from_data(json_message["ticket"])
                image_path = ticket.generate_image()
                # PRINT IMAGE
                self.printer.print(image_path)
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



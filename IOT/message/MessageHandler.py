from GlobalVariables import *
from tools.Timer import Timer
from tools.Sound import PlaySound
from tools.Printer import Printer
from rfid.RfidController import RfidController

class MessageHandler:
    def __init__(self) -> None:

        #* Led controller
        from led.LedController import LEDController
        self.led_trafic = LEDController(pin_numbers=LedPins.instance().trafic_number)
        self.good_led_activities = LEDController(pin_by_name=LedPins.instance().good_rfid_led_number)
        self.error_led_activities = LEDController(pin_by_name=LedPins.instance().error_rfid_led_number)

    def process_message(self, json_message):
        if "type" in json_message:
            if json_message["type"] == "new_request":
                # BLINK TRAFIC LEDS
                self.led_trafic.all_blinking(blinking_repeat=1)
                pass
            elif json_message["type"] == "join":
                # PLAY JOIN SOUND
                PlaySound.join()
                # LIGHT ON ACTIVITY LEDS
                activity_type = json_message["activity_type"]
                rfid_id = RfidController.instance().get_rfid_id_by_text(activity_type)
                self.good_led_activities.on_name(rfid_id)
                pass
            elif json_message["type"] == "leave":
                # PLAY LEAVE SOUND
                PlaySound.leave()
                # LIGHT OFF ACTIVITY LEDS
                activity_type = json_message["activity_type"]
                rfid_id = RfidController.instance().get_rfid_id_by_text(activity_type)
                self.good_led_activities.off_name(rfid_id)
                self.error_led_activities.off_name(rfid_id)
                pass
            elif json_message["type"] == "found":
                # PLAY PRINTING SOUND
                PlaySound.print()
                # LIGHT ON GOOD ACTIVITY LED
                activity_type = json_message["activity_type"]
                rfid_id = RfidController.instance().get_rfid_id_by_text(activity_type)
                time_light_on_seconds = 20
                self.good_led_activities.on_name(rfid_id)
                Timer().start(time_light_on_seconds, self.good_led_activities.off_name, rfid_id)
                #TODO: GENERATE IMAGE
                image_path = "ressources/images/ticket_imprimante.png"
                # PRINT IMAGE
                Printer.print(image_path)
                DLog.LogSuccess(f"Printing of {activity_type} result...")
            elif json_message["type"] == "not_found":
                #TODO: PLAY NOT_FOUND SOUND
                # BLINKING ERROR ACTIVITY LED
                activity_type = json_message["activity_type"]
                rfid_id = RfidController.instance().get_rfid_id_by_text(activity_type)
                self.error_led_activities.blink_name(rfid_id, blinking_repeat=10)
                pass
            else:
                PlaySound.error()
                DLog.LogError("Unknown type")
        elif "uid" in json_message:
            pass
        else:
            DLog.LogError("Can't treat this message")



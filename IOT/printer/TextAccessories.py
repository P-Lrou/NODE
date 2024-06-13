
from tools.Color import Color

class TextHCenter:
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"

class TextAccessories:
    def __init__(self, text: str) -> None:
        self.text = text

        self.rect_position = (0, 0, 100, 100)  # x, y, w, h
        self.h_centered = TextHCenter.LEFT
        self.v_centered = False

        self.size = 10
        self.color = Color.BLACK
        self.font = "arial_black"

    @staticmethod
    def text_activity(text: str):
        text_accessories = TextAccessories(text)
        text_accessories.rect_position = (52, 94, 465, 213)
        text_accessories.h_centered = TextHCenter.CENTER
        text_accessories.v_centered = True

        text_accessories.size = 90
        text_accessories.font = "arial_black"

        return text_accessories
    
    @staticmethod
    def text_hour(text: str):
        text_accessories = TextAccessories(text)
        text_accessories.rect_position = (52, 370, 465, 215)
        text_accessories.h_centered = TextHCenter.CENTER
        text_accessories.v_centered = True

        text_accessories.size = 90
        text_accessories.font = "arial_black"

        return text_accessories
    
    @staticmethod
    def text_participant(text: str, position_x: int, position_y: int):
        text_accessories = TextAccessories(text)
        text_accessories.text = text.replace("-", "\n").replace(" ", "\n")
        width = 210
        height = 117
        x = 52 + position_x * width + position_x * 40
        y = 648 + position_y * height
        text_accessories.rect_position = (x, y, width, height)
        text_accessories.h_centered = TextHCenter.CENTER
        text_accessories.v_centered = True

        text_accessories.size = 26
        text_accessories.font = "arial_black"

        return text_accessories
    
    @staticmethod
    def text_location(text: str, participant_number: int):
        text_accessories = TextAccessories(text)
        y = 955
        if participant_number > 4:
            y += 117
        text_accessories.rect_position = (52, y, 465, 149)
        text_accessories.h_centered = TextHCenter.CENTER
        text_accessories.v_centered = True

        text_accessories.size = 90
        text_accessories.font = "arial_black"

        return text_accessories

class Color:
    BELOTE = (229, 36, 33)
    TRIOMINO = (52, 96, 170)
    SCRABBLE = (251, 187, 14)
    GOUTER = (255, 88, 139)
    PETANQUE = (176, 37, 255)
    PROMENADE = (87, 176, 49)

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    @classmethod
    def get_color_by_text(cls, text):
        text_upper = text.upper()
        if hasattr(cls, text_upper):
            return getattr(cls, text_upper)
        else:
            raise ValueError(f"No color found for text: {text}")

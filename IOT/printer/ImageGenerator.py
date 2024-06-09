from PIL import Image, ImageDraw, ImageFont
from tools.Color import Color
from printer.TextAccessories import TextAccessories, TextHCenter
from GlobalVariables import Path

class ImageGenerator:
    def __init__(self) -> None:
        pass

    def write_text(self, image: Image, text_accessories: TextAccessories, debug: bool = False):
        """
        This method overwrites the image object with the writing text
        """
        def get_font(size: int) -> ImageFont.FreeTypeFont:
            return ImageFont.truetype(font=Path.instance().get_font_path(text_accessories.font), size=size)

        def get_text_dimensions(text_string: str, font: ImageFont.FreeTypeFont) -> tuple[int, int]:
            ascent, descent = font.getmetrics()
            caracters_to_replace = [
                "g", "j", "p", "q", "y"
            ]
            for caracter_to_replace in caracters_to_replace:
                text_string = text_string.replace(caracter_to_replace, "o")
                
            text_width = font.getmask(text_string).getbbox()[2]
            text_height = font.getmask(text_string).getbbox()[3] + descent
            return text_width, text_height

        def text_fits(text: str, font: ImageFont.FreeTypeFont, max_width: int, max_height: int):
            text_width, text_height = get_text_dimensions(text, font)
            return text_width <= max_width and text_height <= max_height

        # Initial font size
        font_size = text_accessories.size
        image_font = get_font(font_size)

        rect_x, rect_y, rect_w, rect_h = text_accessories.rect_position

        # Reduce font size until text fits within the rectangle
        while not text_fits(text_accessories.text, image_font, rect_w, rect_h):
            font_size -= 1
            image_font = get_font(font_size)

        text_image = Image.new('RGBA', (rect_w, rect_h), (0, 0, 0, 0))  # Transparent image
        text_draw = ImageDraw.Draw(text_image)

        anchor: str = ""
        if text_accessories.h_centered == TextHCenter.CENTER:
            x = rect_w/2
            anchor += "m"
        elif text_accessories.h_centered == TextHCenter.LEFT:
            anchor += "l"
            x = 0
        elif text_accessories.h_centered == TextHCenter.RIGHT:
            anchor += "r"
            x = rect_w

        if text_accessories.v_centered:
            anchor += "m"
            y = rect_h/2
        else:
            anchor += "s"
            y = rect_h

        text_draw.text((x, y), text_accessories.text, fill=text_accessories.color, font=image_font, anchor=anchor)

        image.paste(text_image, (rect_x, rect_y), text_image)

        # Draw the debug shapes on the image
        if debug:
            draw = ImageDraw.Draw(image)
            # Print font_size
            print(f"Text: {text_accessories.text}")
            print(f"Font size: {font_size}")
            # Draw the original rectangle (rect_position)
            draw.rectangle([rect_x, rect_y, rect_x + rect_w, rect_y + rect_h], outline=Color.RED, width=1)
        # Save image to check
        image.save(Path.instance().init_image + "test.png")

    def get_image(self, image_name: str) -> Image:
        image = Image.open(Path.instance().init_image + image_name)
        return image
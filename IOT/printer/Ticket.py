from GlobalVariables import Path
from printer.ImageGenerator import ImageGenerator, Image
from printer.TextAccessories import TextAccessories

class Ticket:
    def __init__(self, activity: str, hour: str, participants: list[str], location: str) -> None:
        self.activity = activity.upper()
        self.hour = hour.replace(":", "h").upper()
        self.participants = [participant.upper() for participant in participants]
        self.location = location.upper()
        self.image_generator = ImageGenerator()
        self.top_padding = 250

    def generate_image(self) -> str:
        image_path = f"{Path.instance().init_image}generating/result.png"
        if len(self.participants) > 4:
            image_name = "ticket_6_participants.png"
        else:
            image_name = "ticket_4_participants.png"
        image: Image = self.image_generator.get_image(image_name)
        text_activity = TextAccessories.text_activity(self.activity)
        self.image_generator.write_text(image, text_activity)
        text_hour = TextAccessories.text_hour(self.hour)
        self.image_generator.write_text(image, text_hour)
        for key, participant in enumerate(self.participants):
            if key < 2:
                position_y = 0
            elif key < 4:
                position_y = 1
            else:
                position_y = 2
            if key % 2 == 0:
                position_x = 0
            else:
                position_x = 1
            text_participant = TextAccessories.text_participant(participant, position_x, position_y)
            self.image_generator.write_text(image, text_participant)
        text_location = TextAccessories.text_location(self.location, len(self.participants))
        self.image_generator.write_text(image, text_location)
        width, height = image.size
        final_image = self.image_generator.get_new_image((width, height + self.top_padding), (255, 255, 255, 255))
        final_image = self.image_generator.paste_image(final_image, image, (0, self.top_padding))
        final_image = final_image.rotate(180, expand=1)
        final_image.save(image_path)
        return image_path

    @classmethod
    def from_data(cls, data: dict) -> "Ticket":
        return cls(data.get("activity", ""), data.get("hour", ""), data.get("names", []), data.get("location", "réfectoire"))

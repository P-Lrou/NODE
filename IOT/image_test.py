from printer.Ticket import Ticket
from printer.Printer import ThermalPrinter

data = {
    "activity": "promenade",
    "hour": "14H30",
    "names": [
        "michelle",
        "bertrand",
        "marie",
        "jean-claude",
        "jacques"
    ]
}

ticket = Ticket.from_data(data)
image_path = ticket.generate_image()
printer = ThermalPrinter()
printer.print(image_path)
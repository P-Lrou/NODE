from printer.Ticket import Ticket

data = {
    "activity_type": "promenade",
    "rdv_at": "14H30",
    "names": [
        "michelle",
        "bertrand",
        "marie",
        "jean-claude",
        "jacques"
    ]
}

ticket = Ticket.from_data(data)
ticket.generate_image()
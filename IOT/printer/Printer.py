import subprocess
import RPi.GPIO as GPIO
import time
from printer.phomemo_printer.ESCPOS_printer import Printer

class ThermalPrinter:
    def __init__(self) -> None:
        pass

    def print(self, image_path: str) -> None:
        printer = Printer(bluetooth_address="FD:88:07:60:FF:B1", channel=1)
        printer.print_image(image_path)
        printer.close()

import subprocess
import RPi.GPIO as GPIO
import time
from printer.phomemo_printer.ESCPOS_printer import Printer

class ThermalPrinter:
    def __init__(self) -> None:
        pass

    def print(self, image_path: str) -> None:
        printer = Printer(bluetooth_address="D0:67:6C:D1:DB:6D", channel=1)
        printer.print_image(image_path)
        printer.close()

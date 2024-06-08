import subprocess
import RPi.GPIO as GPIO
import time
from printer.phomemo_printer.ESCPOS_printer import Printer

class ThermalPrinter:
    @staticmethod
    def print(image_path: str) -> None:
        printer = Printer(bluetooth_address="D0:67:6C:D1:DB:6D", channel=1)
        printer.print_image(image_path)
        printer.close()

    @staticmethod
    def switch_state(pin=14):
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(3)
        GPIO.output(pin, GPIO.LOW)

if __name__ == "__main__":
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(14, GPIO.OUT)
    # Printer.switch_state()
    # GPIO.cleanup()
    ThermalPrinter.print("ressources/images/ticket_imprimante.png")
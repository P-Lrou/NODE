import subprocess
import RPi.GPIO as GPIO
import time

class Printer:
    @staticmethod
    def print(image_path: str) -> None:
        command = [
            'phomemo_printer',
            '-a', 'D0:67:6C:D1:DB:6D',
            '-c', '1',
            '-i', image_path
        ]
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    @staticmethod
    def switch_state(pin=18):
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(3)
        GPIO.output(pin, GPIO.LOW)

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
Printer.switch_state()
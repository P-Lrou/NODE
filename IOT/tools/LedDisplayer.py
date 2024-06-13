import RPi.GPIO as GPIO
import time

class LedDisplayer:
    PIN = 17

    @staticmethod
    def setup():
        GPIO.setup(LedDisplayer.PIN, GPIO.OUT)
        GPIO.output(LedDisplayer.PIN, GPIO.LOW)

    @staticmethod
    def new_test_sequence():
        for _ in range(5):
            GPIO.output(LedDisplayer.PIN, GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output(LedDisplayer.PIN, GPIO.LOW)
            time.sleep(0.2)

    @staticmethod
    def test_passed():
        GPIO.output(LedDisplayer.PIN, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(LedDisplayer.PIN, GPIO.LOW)

    @staticmethod
    def test_failed():
        for _ in range(10):
            GPIO.output(LedDisplayer.PIN, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(LedDisplayer.PIN, GPIO.LOW)
            time.sleep(0.5)

    @staticmethod
    def cleanup():
        GPIO.output(LedDisplayer.PIN, GPIO.LOW)
        GPIO.cleanup()
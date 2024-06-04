import RPi.GPIO as GPIO
from rfid.mfrc522 import SimpleMFRC522
from rfid.RfidDelegate import RfidDelegate
from checker.CheckerInterface import CheckerInterface
import spidev
import time

class Rfid(CheckerInterface):
    def __init__(self, pin: int, delegate: RfidDelegate = None, bus=0, device=0, spd=1000000) -> None:
        self.pin = pin
        GPIO.setup(pin, GPIO.OUT)
        self.delegate = delegate

        self.reader = SimpleMFRC522()
        self.bus = bus
        self.device = device
        self.spd = spd
        self.__close()

        self.card_presence = False
        self.array_detect_state = []
        self.last_text_read = None
        self.test_timeout_seconds = 10 

    def __reinit(self):
        self.reader.READER.spi = spidev.SpiDev()
        self.reader.READER.spi.open(self.bus, self.device)
        self.reader.READER.spi.max_speed_hz = self.spd
        self.reader.READER.MFRC522_Init()

    def __open(self):
        GPIO.output(self.pin, GPIO.HIGH)
        self.__reinit()
    
    def __close(self):
        self.reader.READER.spi.close()
        GPIO.output(self.pin, GPIO.LOW)

    def process(self):
        self.__open()
        id, text = self.reader.read_no_block()
        if id:
            self.last_text_read = text.strip()
            rfid_data = {
                "id": id,
                "text": text.replace(" ", "")
            }
            self.array_detect_state = []
            if self.delegate:
                self.delegate.rfid_detected(self, rfid_data)
                if not self.card_presence:
                    self.delegate.rfid_placed(self, rfid_data)
            self.card_presence = True
        else:
            rfid_data = {}
            self.array_detect_state.append(None)
            if len(self.array_detect_state) >= 2:
                self.array_detect_state = []
                if self.delegate:
                    self.delegate.rfid_not_detected(self)
                    if self.card_presence:
                        self.delegate.rfid_removed(self)
                self.card_presence = False
        self.__close()

    def write_no_block(self, text_to_write):
        self.__open()
        id, text = self.reader.write(text_to_write)
        if self.delegate:
            if id:
                self.delegate.rfid_has_written(text)
            else:
                self.delegate.rfid_not_written()
        self.__close()

    def process_checker(self):
        self.__open()
        start_time = time.time()
        try:
            while time.time() - start_time < self.test_timeout_seconds:
                id, text = self.reader.read_no_block()
                if id:
                    self.__close()
                    return True
                time.sleep(0.1)
        except Exception as e:
            pass
        self.__close()
        return False
import RPi.GPIO as GPIO

#* TOOLS
from tools.DLog import DLog

#* RFID
from dock.rfid.mfrc522 import SimpleMFRC522
from dock.rfid.RfidDelegate import RfidDelegate
from dock.rfid.Badge import Badge

from checker.CheckerInterface import CheckerInterface
import spidev
import time

class Rfid(CheckerInterface):
    def __init__(self, pin: int, delegate: RfidDelegate = None, bus=0, device=0, spd=1000000, parent=None) -> None:
        self.pin = pin
        GPIO.setup(pin, GPIO.OUT)
        self.delegate = delegate
        self.parent = parent

        self.reader = SimpleMFRC522()
        self.bus = bus
        self.device = device
        self.spd = spd
        self.__close()

        self.card_presence = False
        self.array_detect_state = []
        self.last_badge_detected: Badge = None
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
            text = text.strip().replace(" ", "")
            if len(text) == 0:
                DLog.LogError("Error to read")
            badge = Badge(id, text)
            self.last_badge_detected = badge
            self.array_detect_state = []
            if self.delegate:
                self.delegate.rfid_detected(badge, self)
                if not self.card_presence:
                    self.delegate.rfid_placed(badge, self)
            self.card_presence = True
        else:
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
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import spidev

class NFC():
    def __init__(self, bus=0, device=0, spd=1000000):
        self.reader = SimpleMFRC522()
        self.close()
        self.boards = {}
        
        self.bus = bus
        self.device = device
        self.spd = spd

    def reinit(self):
        self.reader.READER.spi = spidev.SpiDev()
        self.reader.READER.spi.open(self.bus, self.device)
        self.reader.READER.spi.max_speed_hz = self.spd
        self.reader.READER.MFRC522_Init()

    def close(self):
        self.reader.READER.spi.close()

    def addBoard(self, rid, pin):
        GPIO.setup(pin, GPIO.OUT)
        self.boards[rid] = pin

    def selectBoard(self, rid):
        if not rid in self.boards:
            print("readerid " + rid + " not found")
            return False

        for loop_id in self.boards:
            gpio_state = GPIO.HIGH if loop_id == rid else GPIO.LOW
            GPIO.output(self.boards[loop_id], gpio_state)
        return True

    def read(self, rid):
        if not self.selectBoard(rid):
            return None

        self.reinit()
        cid, val = self.reader.read_no_block()
        print(f"{rid}: {cid}")
        self.close()

        return val

    def write(self, rid, value):
        if not self.selectBoard(rid):
            return False

        self.reinit()
        self.reader.write_no_block(value)
        self.close()
        return True


if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    nfc = NFC()
    try:
        nfc.addBoard("reader1",2)
        nfc.addBoard("reader2",3)
        nfc.addBoard("reader3",4)
        while True:
            data = nfc.read("reader1")
            data = nfc.read("reader2")
            data = nfc.read("reader3")
    except KeyboardInterrupt:
        pass

    GPIO.cleanup()
from platform import system
from time import sleep
from serial import STOPBITS_TWO, Serial

from pydmx.controller.controller import OS, DMXController, operatingsystem

if operatingsystem == OS.LINUX:
    import fcntl


class SerialController(DMXController):
    def __init__(self, port: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # The port name and index differs from OS to OS
        self.port = self._check_port(port)
        # The standard serial settings from pySerial can many be left as is:
        # Baudrate: 250000 (standard: 9600)
        # Bytesize: EIGHTBITS
        # Parity: PARITY_NONE
        # StopBits: STOPBITS_TWO (standard: STOPBITS_ONE)
        self.serial = Serial(port, baudrate=250000, stopbits=STOPBITS_TWO)
        self.thread.start()

    def _check_port(self, port: str) -> str:
        # TODO: Portchecking
        return "COM3"

    def write(self):
        if operatingsystem == OS.LINUX:
            fcntl.ioctl(self.desc, 0x5427)
            sleep(0.0001)
            fcntl.ioctl(self.desc, 0x5428)
        else:
            self.serial.send_break(0.0001)
        self.serial.write(b'\x00')
        self.serial.write(self._dmxdata)
        self.serial.flush()

    @staticmethod
    def get_controller_name() -> str:
        return "SerialController"

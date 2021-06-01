from os import path
from platform import system
from typing import List

from pylibftdi import Device, Driver, LibraryMissingError

from pydmx.controller.controller import DMXController

if system() == "Linux":

    from ctypes import Structure, byref, c_long, cdll

    DRIVER_PATH = path.abspath(path.dirname(__file__))
    Driver._lib_search["libftdi"] = tuple(
        [
            path.join(DRIVER_PATH, "libftdi.so"),
            path.join(DRIVER_PATH, "libftdi.so.1"),
            path.join(DRIVER_PATH, "libftdi1.so"),
        ]
        + list(Driver._lib_search["libftdi"])
    )

    _LIBC = cdll.LoadLibrary("libc.so.6")

    class timespec(Structure):
        """A timespec."""

        _fields_ = [("tv_sec", c_long), ("tv_nsec", c_long)]

    def wait_ms(milliseconds):
        """Wait for a specified number of milliseconds."""
        dummy = timespec()
        sleeper = timespec()
        sleeper.tv_sec = int(milliseconds / 1000)
        sleeper.tv_nsec = (milliseconds % 1000) * 1000000
        _LIBC.nanosleep(byref(sleeper), byref(dummy))

    def wait_us(nanoseconds):
        """Wait for a specified number of nanoseconds."""
        dummy = timespec()
        sleeper = timespec()
        sleeper.tv_sec = int(nanoseconds / 1000000)
        sleeper.tv_nsec = (nanoseconds % 1000) * 1000
        _LIBC.nanosleep(byref(sleeper), byref(dummy))


elif system() == "Windows":

    from ctypes import byref, windll, wintypes

    _WIN32 = windll.kernel32
    _MS = 1000000
    _INFINITE = 0xFFFFFFFF

    def wait_ms(milliseconds):
        """Wait for a specified number of milliseconds."""
        wait_time = wintypes.LARGE_INTEGER(-(_MS * abs(milliseconds)))
        timer_handle = _WIN32.CreateWaitableTimerW(None, True, None)
        if timer_handle == 0:
            raise Exception("CreateWaitableTimerW returned NULL")
        if (
            _WIN32.SetWaitableTimer(
                timer_handle, byref(wait_time), 0, None, None, False
            )
            == 0
        ):
            raise Exception("SetWaitableTimer returned 0")
        _WIN32.WaitForSingleObject(timer_handle, _INFINITE)
        _WIN32.CloseHandle(timer_handle)

    def wait_us(nanoseconds):
        """Wait for a specified number of nanoseconds."""
        wait_time = wintypes.LARGE_INTEGER(-abs(nanoseconds))
        timer_handle = _WIN32.CreateWaitableTimerW(None, True, None)
        if timer_handle == 0:
            raise Exception("CreateWaitableTimerW returned NULL")
        if (
            _WIN32.SetWaitableTimer(
                timer_handle, byref(wait_time), 0, None, None, False
            )
            == 0
        ):
            raise Exception("SetWaitableTimer returned 0")
        _WIN32.WaitForSingleObject(timer_handle, _INFINITE)
        _WIN32.CloseHandle(timer_handle)


class FTDI(Device, DMXController):

    _BITS_8 = 8
    _STOP_BITS_2 = 2
    _PARITY_NONE = 0
    _BREAK_OFF = 0
    _BREAK_ON = 1

    def __init__(self, device_index=0):
        """
            Constructor for the FTDI Class

            Parameters:
                device_index (int): The Device index of the FTDI
        """

        # TODO: Check for device before assigning device_index
        try:
            Device.__init__(self, mode="b", device_index=device_index)
        except LibraryMissingError:
            raise Exception(
                "Dependency libftdi not found. Check the README for driver dependencies."
            )
        self.baudrate = DMXController._BAUD_RATE
        self.ftdi_fn.ftdi_set_line_property(
            DMXController._BIT_ENCODING,
            DMXController._STOP_BIT_LENGTH,
            DMXController._PARITY_BIT_LENGTH,
        )

    def write(self, data: List[int]):
        """Write 512 bytes or less of DMX data."""
        try:
            data = [136, 0, 136, 0, 136, 0, 0, 0, 0, 0]
            byte_data = bytes(data)
            print(byte_data)
        except TypeError:
            byte_data = self.encoder.encode(data)
        # Break
        self._set_break_on()
        wait_ms(10)
        # Mark after break
        self._set_break_off()
        wait_us(8)
        # Frame body
        Device.write(self, b"\x00" + byte_data)
        # Idle
        wait_ms(15)

    def _set_break_on(self):
        self.ftdi_fn.ftdi_set_line_property2(
            DMXController._BIT_ENCODING,
            DMXController._STOP_BIT_LENGTH,
            DMXController._PARITY_BIT_LENGTH,
            FTDI._BREAK_ON,
        )

    def _set_break_off(self):
        self.ftdi_fn.ftdi_set_line_property2(
            DMXController._BIT_ENCODING,
            DMXController._STOP_BIT_LENGTH,
            DMXController._PARITY_BIT_LENGTH,
            FTDI._BREAK_OFF,
        )

    @staticmethod
    def get_controller_name() -> str:
        """Get controller name."""
        return "FTDI"


def get_ftdi_device_list():
    """
    return a list of lines, each a colon-separated
    vendor:product:serial summary of detected devices
    """
    dev_list = []
    for device in Driver().list_devices():
        # list_devices returns bytes rather than strings
        dev_info = map(lambda x: x.decode("latin1"), device)
        # device must always be this triple
        vendor, product, serial = dev_info
        dev_list.append("%s:%s:%s" % (vendor, product, serial))
    return dev_list

import time

from pydmx.controller.serial import SerialController

sender = SerialController("COM3")
sender.activate()
sender.dmxdata = bytes((100, 0, 200, 0, 0, 0, 0, 0) * 64)
time.sleep(5)

from pydmx.controller.serial import SerialController
import time

sender = SerialController("COM3")
sender.activate()
sender.dmxdata = bytes((100,100,0,0,100,0,0,0)*64)
time.sleep(5)

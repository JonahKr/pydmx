from abc import ABC, abstractmethod

from typing import List


class DMXController(ABC):
    """
  DMX Controller Base Class
  """

    """
  Source: DMX512 Protocol Implementation Using MC9S08GT60 8-Bit MCU By NXP
    https://web.archive.org/web/20170830235842/http://cache.freescale.com/files/microcontrollers/doc/app_note/AN3315.pdf
  
    2. DMX512 Protocol Overview:
      The DMX512 protocol is simple because it is an asynchronous 8-bit serial protocol and works in an
      unidirectional line generated by a master device (or console). The protocol can handle up to 512 devices
      in a DMX network and communicates at 250 kbps baud rate. Each bit in the frame is generated every 4us.
    
    2.2 Data Protocol:


  """
    _BAUD_RATE = 250000
    _BIT_ENCODING = 8
    _START_BIT_LENGTH = 1
    _STOP_BIT_LENGTH = 2
    _PARITY_BIT_LENGTH = 0

    @abstractmethod
    def __init__(self, *args, **kwargs):
        """
    Initialising the DMX Controller
    """

    @abstractmethod
    def write(self, dmxdata: List[int]):
        """
    Writing 512 Bytes of DMX Data
    """

    @staticmethod
    def get_controller_name():
        return "ABC"

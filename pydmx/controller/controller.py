from abc import ABC, abstractmethod

import numpy as np

class DMXController(ABC):
  """
  DMX Controller Base Class
  """

  """
  Source: https://web.archive.org/web/20170830235842/http://cache.freescale.com/files/microcontrollers/doc/app_note/AN3315.pdf
  """
  _BAUD_RATE = 250000
  _BIT_ENCODING = 8
  _START_BIT_LENGTH = 1


  @abstractmethod
  def __init__(self, *args, **kwargs):
    """
    Initialising the DMX Controller
    """
  
  @abstractmethod
  def write(self, dmxdata: np.ndarray):
    """
    Writing 512 Bytes of DMX Data
    """
  
  @staticmethod
  def get_controller_name():
    return "ABC"

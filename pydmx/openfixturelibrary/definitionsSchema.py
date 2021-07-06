"""
Standard non purpose related schemas.
"""
from typing import NamedTuple


class Dimensions(NamedTuple):
    """X,Y,Z Dimensions"""

    x: float
    y: float
    z: float


class MinMax(NamedTuple):
    """Minimum and maximum values"""

    minimum: int
    maximum: int

class Color(Enum):
    """Enum: All default Colors."""
    RED = "Red"
    GREEN = "Green"
    BLUE = "Blue"
    CYAN = "Cyan"
    MAGENTA = "Magenta"
    YELLOW = "Yellow"
    AMBER = "Amber"
    WHITE = "White"
    WARMWHITE = "Warm White"
    COLDWHITE = "Cold White"
    UV = "UV"
    LIME = "Lime"
    INDIGO = "Indigo"
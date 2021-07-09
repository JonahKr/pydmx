"""
Standard non purpose related schemas.
"""
from dataclasses import dataclass
from typing import NamedTuple, Optional
from enum import Enum

@dataclass
class Angle:
    """
    Degrees, Percent or Enum:
    beamAngle: ["closed", "narrow", "wide"]
    horizontalAngle: ["left", "center", "right"]
    verticalAngle: ["top", "center", "bottom"]
    swingAngle: ["closed", "narrow", "wide"]
    """

    angle: str
    angleStart: str
    angleEnd: str


@dataclass
class Brightness:
    """Brightness in lumens, percent, "enum":["off", "dark", "bright"]"""

    brightness: Optional[str]
    brightnessStart: Optional[str]
    brightnessEnd: Optional[str]


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


@dataclass
class ColorTemperatureType:
    """Color Temperature in kelvin, percent, "enum": ["warm", "CTO", "default", "cold", "CTB"]"""

    colorTemperature: Optional[str]
    colorTemperatureStart: Optional[str]
    colorTemperatureEnd: Optional[str]


class Dimensions(NamedTuple):
    """X,Y,Z Dimensions"""

    x: float
    y: float
    z: float


@dataclass
class Duration:
    """Duration in seconds, milliseconds,percent, "enum": ["instant", "short", "long"]"""

    duration: Optional[str]
    durationStart: Optional[str]
    durationEnd: Optional[str]


class MinMax(NamedTuple):
    """Minimum and maximum values"""

    minimum: int
    maximum: int


@dataclass
class Speed:
    """Speed in hertz, beatsPerMinute, percent, "enum": ["fast", "slow", "stop", "slow reverse", "fast reverse"]"""

    speed: Optional[str]
    speedStart: Optional[str]
    speedEnd: Optional[str]

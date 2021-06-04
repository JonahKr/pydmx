# TODO rethink the Logic of using different Base Classes for the different Capabilities

from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, Optional, Union

from pydmx.fixture.fixtureSchema import MinMax

Capability = Union[ColorIntensity, ShutterStrobe]


class CapabilityType(Enum):
    NOFUNCTION = auto()
    SHUTTERSTROBE = auto()
    STROBESPEED = auto()
    STROBEDURATION = auto()
    INTENSITY = auto()
    COLORINTENSITY = auto()
    COLORPRESET = auto()
    COLORTEMPERATURE = auto()
    PAN = auto()
    PANCONTINUOUS = auto()
    TILT = auto()
    TILTCONTINUOUS = auto()
    PANTILTSPEED = auto()
    WHEELSLOT = auto()
    WHEELSHAKE = auto()
    WHEELSLOTROTATION = auto()
    WHEELROTATION = auto()
    EFFECT = auto()
    EFFECTSPEED = auto()
    EFFECTDURATION = auto()
    EFFECTPARAMETER = auto()
    SOUNDSENSITIVITY = auto()
    BEAMANGLE = auto()
    BEAMPOSITION = auto()
    FOCUS = auto()
    ZOOM = auto()
    IRIS = auto()
    IRISEFFECT = auto()
    FROST = auto()
    FROSTEFFECT = auto()
    PRISM = auto()
    PRISMROTATION = auto()
    BLADEINSERTION = auto()
    BLADEROTATION = auto()
    BLADESYSTEMROTATION = auto()
    FOG = auto()
    FOGTYPE = auto()
    ROTATION = auto()
    SPEED = auto()
    TIME = auto()
    MAINTENANCE = auto()
    GENERIC = auto()


@dataclass
class CapabilitySchema:
    # Range of DMX values e.g. 0 to 255 (in most cases) the capability can be applied at
    dmxRange: Optional[MinMax]
    # Comment with further descriptions
    comment: Optional[str]
    # If the fixture entry needs some love
    helpWanted: Optional[str]
    #
    menuclick: Optional[MenuClick]
    # A switching channel is a channel whose functionality depends on the value of another channel in the same mode.
    switchChannels: Optional[Dict[str, str]]
    # Capability from the list above
    _type: CapabilityType


class MenuClick(Enum):
    START = auto()
    CENTER = auto()
    END = auto()
    HIDDEN = auto()


@dataclass
class ColorIntensity(CapabilitySchema):
    _type = CapabilityType.COLORINTENSITY
    color: Color
    # Brightness either in Lumens or Percent
    brightness: Optional[str]
    brightnessStart: Optional[str]
    brightnessEnd: Optional[str]


class Color(Enum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()
    CYAN = auto()
    MAGENTA = auto()
    YELLOW = auto()
    AMBER = auto()
    WHITE = auto()
    WARMWHITE = auto()
    COLDWHITE = auto()
    UV = auto()
    LIME = auto()
    INDIGO = auto()


@dataclass
class ShutterStrobe(CapabilitySchema):
    _type = CapabilityType.SHUTTERSTROBE
    shutterEffect: ShutterEffect
    soundControlled: Optional[bool]
    # Speed in hertz, beatsPerMinute, percent, "enum": ["fast", "slow", "stop", "slow reverse", "fast reverse"]
    speed: Optional[str]
    speedStart: Optional[str]
    speedEnd: Optional[str]
    # Duration in seconds, milliseconds,percent, "enum": ["instant", "short", "long"]
    duration: Optional[str]
    durationStart: Optional[str]
    durationEnd: Optional[str]
    randomTiming: Optional[bool]


class ShutterEffect(Enum):
    OPEN = auto()
    CLOSED = auto()
    STROBE = auto()
    PULSE = auto()
    RAMPUP = auto()
    RAMPDOWN = auto()
    RAMPUPDOWN = auto()
    LIGHTNING = auto()
    SPIKES = auto()

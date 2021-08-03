from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Union

from pydmx.openfixturelibrary.definitionsSchema import (
    Angle,
    Brightness,
    Color,
    ColorTemperatureType,
    Duration,
    MinMax,
    Speed,
)


class CapabilityType(Enum):
    """Enum: All possible channel capabilities"""

    NOFUNCTION = "NoFunction"
    SHUTTERSTROBE = "ShutterStrobe"
    STROBESPEED = "StrobeSpeed"
    STROBEDURATION = "StrobeDuration"
    INTENSITY = "Intensity"
    COLORINTENSITY = "ColorIntensity"
    COLORPRESET = "ColorPreset"
    COLORTEMPERATURE = "ColorTemperature"
    PAN = "Pan"
    PANCONTINUOUS = "PanContinuous"
    TILT = "Tilt"
    TILTCONTINUOUS = "TiltContinuous"
    PANTILTSPEED = "PanTiltSpeed"
    WHEELSLOT = "WheelSlot"
    WHEELSHAKE = "WheelShake"
    WHEELSLOTROTATION = "WheelSlotRotation"
    WHEELROTATION = "WheelRotation"
    EFFECT = "Effect"
    EFFECTSPEED = "EffectSpeed"
    EFFECTDURATION = "EffectDuration"
    EFFECTPARAMETER = "EffectParameter"
    SOUNDSENSITIVITY = "SoundSensitivity"
    BEAMANGLE = "BeamAngle"
    BEAMPOSITION = "BeamPosition"
    FOCUS = "Focus"
    ZOOM = "Zoom"
    IRIS = "Iris"
    IRISEFFECT = "IrisEffect"
    FROST = "Frost"
    FROSTEFFECT = "FrostEffect"
    PRISM = "Prism"
    PRISMROTATION = "PrismRotation"
    BLADEINSERTION = "BladeInsertion"
    BLADEROTATION = "BladeRotation"
    BLADESYSTEMROTATION = "BladeSystemRotation"
    FOG = "Fog"
    FOGOUTPUT = "FogOutput"
    FOGTYPE = "FogType"
    ROTATION = "Rotation"
    SPEED = "Speed"
    TIME = "Time"
    MAINTENANCE = "Maintenance"
    GENERIC = "Generic"


class MenuClick(Enum):
    """Enum: different menu clicks"""

    START = "start"
    CENTER = "center"
    END = "end"
    HIDDEN = "hidden"


@dataclass
class CapabilitySchema:
    """Parent Schema for all Capabilities"""

    # Range of DMX values e.g. 0 to 255 (in most cases) the capability can be applied at
    dmxRange: Optional[MinMax]
    # Capability from the list above
    # type: CapabilityType
    # Comment with further descriptions
    comment: Optional[str]
    # If the fixture entry needs some love
    helpWanted: Optional[str]
    #
    menuclick: Optional[MenuClick]
    # A switching channel is a channel whose functionality depends on the value of another channel in the same mode.
    switchChannels: Optional[Dict[str, str]]


#
# NoFunction
#
@dataclass
class NoFunction(CapabilitySchema):
    type: CapabilityType = CapabilityType.NOFUNCTION


#
# ShutterStrobe
#
class ShutterEffect(Enum):
    """Enum: All predefined shutter strobe effects"""

    OPEN = "Open"
    CLOSED = "Closed"
    STROBE = "Strobe"
    PULSE = "Pulse"
    RAMPUP = "RampUp"
    RAMPDOWN = "RampDown"
    RAMPUPDOWN = "RampUpDown"
    LIGHTNING = "Lightning"
    SPIKES = "Spikes"


@dataclass
class ShutterStrobe(CapabilitySchema, Speed, Duration):
    shutterEffect: ShutterEffect
    # Sound COntroll Toggle
    soundControlled: Optional[bool]
    randomTiming: Optional[bool]
    type: CapabilityType = CapabilityType.SHUTTERSTROBE


#
# StrobeSpeed
#
@dataclass
class StrobeSpeed(CapabilitySchema, Speed):
    type: CapabilityType = CapabilityType.STROBESPEED


#
# StrobeDuration
#
@dataclass
class StrobeDuration(CapabilitySchema, Duration):
    type: CapabilityType = CapabilityType.STROBEDURATION


#
# Intensity
#
@dataclass
class Intensity(CapabilitySchema, Brightness):
    type: CapabilityType = CapabilityType.INTENSITY


#
# ColorIntensity
#
@dataclass
class ColorIntensity(CapabilitySchema, Brightness):
    color: Color
    type: CapabilityType = CapabilityType.COLORINTENSITY


#
# ColorPreset
#
@dataclass
class ColorPreset(CapabilitySchema, ColorTemperatureType):
    colors: Optional[List[str]]
    colorsStart: Optional[List[str]]
    colorsEnd: Optional[List[str]]
    type: CapabilityType = CapabilityType.COLORPRESET


#
# ColorTemperature
#
@dataclass
class ColorTemperature(CapabilitySchema, ColorTemperatureType):
    type: CapabilityType = CapabilityType.COLORTEMPERATURE


#
# Pan
#
@dataclass
class Pan(CapabilitySchema, Angle):
    type: CapabilityType = CapabilityType.PAN


#
# PanContinuous
#
@dataclass
class PanContinuous(CapabilitySchema, Speed):
    type: CapabilityType = CapabilityType.PANCONTINUOUS


#
# Tilt
#
@dataclass
class Tilt(CapabilitySchema, Angle):
    type: CapabilityType = CapabilityType.TILT


Capabilities = Union[
    NoFunction,
    ShutterStrobe,
    StrobeSpeed,
    StrobeDuration,
    Intensity,
    ColorIntensity,
    ColorPreset,
    ColorTemperature,
    Pan,
    PanContinuous,
    Tilt,
]

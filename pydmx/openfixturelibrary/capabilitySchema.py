# TODO rethink the Logic of using different Base Classes for the different Capabilities

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional, Union

from pydmx.openfixturelibrary.definitionsSchema import MinMax, Color


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
    type: CapabilityType
    # Comment with further descriptions
    comment: Optional[str]
    # If the fixture entry needs some love
    helpWanted: Optional[str]
    # 
    menuclick: Optional[MenuClick]
    # A switching channel is a channel whose functionality depends on the value of another channel in the same mode.
    switchChannels: Optional[Dict[str, str]]

@dataclass
class ColorIntensity(CapabilitySchema):
    type = CapabilityType.COLORINTENSITY
    #
    color: Color
    # Brightness either in Lumens or Percent
    brightness: Optional[str]
    brightnessStart: Optional[str]
    brightnessEnd: Optional[str]


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
    OPEN = ""
    CLOSED = ""
    STROBE = ""
    PULSE = ""
    RAMPUP = ""
    RAMPDOWN = ""
    RAMPUPDOWN = ""
    LIGHTNING = ""
    SPIKES = ""

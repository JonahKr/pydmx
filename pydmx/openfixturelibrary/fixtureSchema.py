"""
Python Schemas for defining a fixture


The Python Schema is based on the fixture Definition of the open-fixture-library:
https://raw.githubusercontent.com/OpenLightingProject/open-fixture-library/master/schemas/fixture.json

Current Version: 12.2.2
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydmx.openfixturelibrary.channelSchema import ChannelSchema
from pydmx.openfixturelibrary.definitionsSchema import Dimensions, MinMax


class FixtureCategories(Enum):
    """Enum: All possible Categories for fixtures."""

    BARRELSCANNER = "Barrel Scanner"
    BLINDER = "Blinder"
    COLORCHANGER = "Color Changer"
    DIMMER = "Dimmer"
    EFFECT = "Effect"
    FAN = "Fan"
    FLOWER = "Flower"
    HAZER = "Hazer"
    LASER = "Laser"
    MATRIX = "Matrix"
    MOVINGHEAD = "Moving Head"
    PIXELBAR = "Pixel Bar"
    SCANNER = "Scanner"
    SMOKE = "Smoke"
    STAND = "Stand"
    STROBE = "Strobe"
    OTHER = "Other"


@dataclass
class ImportPluginSchema:
    """Metadata about how the fixture entry got imported."""

    # Plugin the Schema got imported from e.g. qlcplus_4.12.1
    plugin: str
    # isoDateString
    date: str
    # Multiline Comment
    comment: Optional[str]


@dataclass
class MetaSchema:
    """Metadata about the fixture entry."""

    # list of the authors of the fixture
    authors: List[str]
    # isoDateString e.g. 2020-09-20
    createDate: str
    # isoDateString e.g. 2020-09-20
    lastModifyDate: str
    # if the Schema got imported from a specific software
    importPlugin: Optional[ImportPluginSchema]


@dataclass
class LinksSchema:
    """Collection of Links to various Ressources"""

    # Link to the the Manual of the fixture as url
    manual: Optional[List[str]]
    # Link to the product Page of the manufacturer as url
    productPage: Optional[List[str]]
    # Link to example Video as url
    video: Optional[List[str]]
    # Link to additional Ressources as url
    other: Optional[List[str]]


@dataclass
class RDMSchema:
    """If the fixture supports RDM, the modelId is required: https://www.rdmprotocol.org/rdm/what-is-rdm/"""

    # The model id of the RDM supporting fixture: value between 0 and 65535
    modelId: int
    # The SoftwareVersion of RDM the fixture can support
    softwareVersion: Optional[str]


class DMXConnector(Enum):
    """Enum: All selectable DMX Connectors"""

    THREEPIN = "3-pin"
    THREEPINSWAPPED = "3-pin (swapped +/-)"
    THREEPINXLR = "3-pin XLR IP65"
    FIVEPIN = "5-pin"
    FIVEPINXLR = "5-pin XLR IP65"
    THREEFIVEPIN = "3-pin and 5-pin"
    STEREOJACK = "3.5mm stereo jack"


@dataclass
class BulbSchema:
    """Information about the Bulbs in the fixture"""

    # e.g. LED
    type: Optional[str]
    # Temperature of the Color in Kelvin
    colorTemperatur: Optional[int]
    # Lumens of the bulb
    lumens: Optional[int]


@dataclass
class LensSchema:
    """Specifics about the Lens in the fixture"""

    # e.g. 'PC', 'Fresnel
    name: Optional[str]
    # Maximum and Minimum degrees of Lens from 0 to 360
    degreesMinMax: Optional[MinMax]


@dataclass
class MatrixPixelsSchema:
    """Additional dimension data about a LED-matrix"""

    dimensions: Optional[Dimensions]
    spacing: Optional[Dimensions]


@dataclass
class PhysicalSchema:
    """Physical properties of a fixture"""

    # The Dimensions of the Fixture x,y,z
    dimensions: Optional[Dimensions]
    # Weight in kg
    weight: Optional[float]
    # power consumption in Watts
    power: Optional[int]
    # Physical DMX Connector Types: THREEPIN, FIVEPINXLR
    dmxConnector: Optional[DMXConnector]
    # Extra info about the built in bulb
    bulb: Optional[BulbSchema]
    # Extra info about the built in lens
    lens: Optional[LensSchema]
    # Extra dimension info about the Pixel matrix
    matrixPixels: Optional[MatrixPixelsSchema]


class RepeatFor(Enum):
    """Enum:Repeat for options"""

    EACHPIXELABC = "eachPixelABC"
    EACHPIXELXYZ = "eachPixelXYZ"
    EACHPIXELXZY = "eachPixelXZY"
    EACHPIXELYXZ = "eachPixelYXZ"
    EACHPIXELYZX = "eachPixelYZX"
    EACHPIXELZXY = "eachPixelZXY"
    EACHPIXELZYX = "eachPixelZYX"
    EACHPIXELGROUP = "eachPixelGroup"


class ChannelOrder(Enum):
    """Enum: Channel order options"""

    PERPIXEL = "perPixel"
    PERCHANNEL = "perChannel"


@dataclass
class MatrixChannels:
    """Custom channel setting extensions for matrix fixtures"""

    repeatFor: Union[RepeatFor, List[str]]
    channelOrder: ChannelOrder
    templateChannels: List[Union[None, str]]
    insert: str = "matrixChannels"


@dataclass
class ModesSchema:
    """Defining the choosable modes for a fixture."""

    name: str
    shortName: Optional[str]
    rdmPersonalityIndex: Optional[int]
    physical: Optional[PhysicalSchema]
    channels: List[Union[None, str, MatrixChannels]]


@dataclass
class FixtureSchema:
    """Python Schema of a DMX fixture following the open-fixture-library schemas"""

    # unique in manufacturer
    name: str
    # unique in OpenFixtureLibrary
    shortName: Optional[str]
    # most important category first. All items are unique.
    categories: List[FixtureCategories]
    # information about the fixture entry
    meta: MetaSchema
    # Comment with additional Information about the fixture
    comment: Optional[str]
    # Links to additional ressources about the fixture
    links: Optional[LinksSchema]
    # If the fixture entry needs some love
    helpWanted: Optional[str]
    # If the fixture supports RDM
    rdm: Optional[RDMSchema]
    # Physical descriptions of the fixture e.g. mass, size, bulb etc...
    physical: Optional[PhysicalSchema]
    # TODO: Matrix Schema
    matrix: Optional[Any]
    # TODO: Wheel Schema
    wheels: Optional[Any]
    # List of all the available Channels with their settings for the fixture
    availableChannels: Optional[Dict[str, ChannelSchema]]
    # Template Channels
    templateChannels: Optional[Dict[str, ChannelSchema]]
    # Mode
    modes: List[ModesSchema]

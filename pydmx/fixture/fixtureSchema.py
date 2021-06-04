"""

"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, NamedTuple, Optional

from pydmx.fixture.channelSchema import ChannelSchema


@dataclass
class FixtureSchema:
    """
  Following the Fixture Schema from the OpenFixtureLibrary
  Version: 12.2.1
  More Infos here: https://github.com/OpenLightingProject/open-fixture-library/blob/master/docs/fixture-format.md
  """

    # unique in manufacturer
    name: str
    # unique in OpenFixtureLibrary
    shortName: str
    # most important category first. All items are unique.
    categories: List[FixtureCategories]
    # information about the fixture entry
    meta: MetaSchema
    # Comment with additional Information about the fixture
    comment: Optional[str]
    # Links to additional ressources about the fixture
    links: LinkSchema
    # If the fixture entry needs some love
    helpWanted: str
    # If the fixture supports RDM
    rdm: Optional[RDMSchema]
    # Physical descriptions of the fixture e.g. mass, size, bulb etc...
    physical: Optional[PhysicalSchema]
    # TODO: Matrix Schema
    matrix: Optional[str]
    # TODO: Wheel Schema
    wheels: Optional[str]
    # List of all the available Channels with their settings for the fixture
    availableChannels: Dict[
        str,
    ]


class FixtureCategories(Enum):
    BARRELSCANNER = auto()
    BLINDER = auto()
    COLORCHANGER = auto()
    DIMMER = auto()
    EFFECT = auto()
    FAN = auto()
    FLOWER = auto()
    HAZER = auto()
    LASER = auto()
    MATRIX = auto()
    MOVINGHEAD = auto()
    PIXELBAR = auto()
    SCANNER = auto()
    SMOKE = auto()
    STAND = auto()
    STROBE = auto()
    OTHER = auto()


@dataclass
class MetaSchema:
    """Metadata about the fixture entry."""

    authors: List[str]
    # isoDateString e.g. 2020-09-20
    createDate: str
    # isoDateString e.g. 2020-09-20
    lastModifyDate: str
    # if the Schema got imported from a specific software
    importPlugin: Optional[ImportPluginSchema]


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
class LinkSchema:
    """Collection of Links to various Ressources"""

    # Link to the the Manual of the fixture
    manual: Optional[List[str]]
    # Link to the product Page of the manufacturer
    productPage: Optional[List[str]]
    # Link to example Video
    video: Optional[List[str]]
    # Link to additional Ressources
    other: Optional[List[str]]


@dataclass
class RDMSchema:
    """If the fixture supports RDM, the modelId is required: https://www.rdmprotocol.org/rdm/what-is-rdm/"""

    # The model id of the RDM supporting fixture: value between 0 and 65535
    modelId: int
    # The SoftwareVersion of RDM the fixture can support
    softwareVersion: Optional[str]


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
    DMXConnector: Optional[PhysicalDMXConnector]
    # Extra info about the built in bulb
    bulb: Optional[BulbSchema]
    # Extra info about the built in lens
    lens: Optional[LensSchema]
    # Extra dimension info about the Pixel matrix
    matrixPixels: Optional[MatrixSchema]


class Dimensions(NamedTuple):
    """X,Y,Z Dimensions"""

    x: float
    y: float
    z: float


class PhysicalDMXConnector(Enum):
    THREEPIN = auto()
    THREEPINSWAPPED = auto()
    THREEPINXLR = auto()
    FIVEPIN = auto()
    FIVEPINXLR = auto()
    THREEFIVEPIN = auto()
    STEREOJACK = auto()


@dataclass
class BulbSchema:
    """Information about the Bulbs in the fixture"""

    # e.g. LED
    _type: Optional[str]
    # Temperature of the Color in Kelvin
    colorTemperatur: Optional[int]
    # Lumens of the bulb
    lumens: Optional[int]


@dataclass
class LensSchema:
    """Specifics about the Lens in the fixture"""

    # e.g. 'PC', 'Fresnel
    name: Optional[str]
    #
    degreesMinMax: Optional[MinMax]


class MinMax(NamedTuple):
    """Minimum and maximum values"""

    _min: int
    _max: int


@dataclass
class MatrixSchema:
    """Additional dimension data about a LED-matrix"""

    dimensions: Optional[Dimensions]
    spacing: Optional[Dimensions]

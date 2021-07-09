from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Union

from pydmx.openfixturelibrary.capabilitySchema import Capabilities


class DmxResolution(Enum):
    """Enum: The DMX bit resolution options."""

    EIGHTBIT = "8bit"
    SIXTEENBIT = "16bit"
    TWENTYFOURBIT = "24bit"


class Precedence(Enum):
    """Enum: Precedence specifies to which value the channel should be set if there are two conflicting active cues containing this channel"""

    # Latest takes presendece
    LTP = "LTP"
    # Highest takes Presedence
    HTP = "HTP"


@dataclass
class ChannelSchema:
    """Definition of a specific Channel of a fixture"""

    # Channel name
    name: Optional[str]
    # fineChannelAliases
    fineChannelAliases: Optional[List[str]]
    # The DMX Resolution of the Channel
    dmxValueResolution: Optional[DmxResolution]
    # Default Value of the Channel either as a number or in percent
    defaultValue: Optional[Union[int, str]]
    # Highlight Value of the Channel either as a number or in percent
    highlightValue: Optional[Union[int, str]]
    # If constant is true, the channel should be set to a static value in the operating lighting program
    constant: Optional[bool]
    # precedence specifies to which value the channel should be set if there are two conflicting active cues containing this channel:
    # HTP (Highest takes precedence) or LTP (Latest (change) takes precedence).
    precedence: Optional[Precedence]
    # The Capability of this Channel
    capability: Optional[Capabilities]
    # Capabilities of the Channel if multiple are defined
    capabilities: Optional[List[Capabilities]]

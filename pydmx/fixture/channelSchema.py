from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Union

from pydmx.fixture.capability import Capability


@dataclass
class ChannelSchema:
    #
    name: Optional[str]
    # TODO: fineChannelAliases
    # The DMX Resolution of the Channel
    dmxValueResolution: Optional[dmxResolution]
    # Default Value of the Channel either as a number or in percent
    defaultValue: Union[int, str]
    # Highlight Value of the Channel either as a number or in percent
    highlightValue: Optional[Union[int, str]]
    # If constant is true, the channel should be set to a static value in the operating lighting program
    constant: bool
    # recedence specifies to which value the channel should be set if there are two conflicting active cues containing this channel:
    # HTP (Highest takes precedence) or LTP (Latest (change) takes precedence).
    precedence: Optional[str]
    # The Capability of this Channel
    capability: Capability


class dmxResolution(Enum):
    EIGHTBIT = auto()
    SIXTEENBIT = auto()
    TWENTYFOURBIT = auto()

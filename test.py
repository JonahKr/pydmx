import json
from abc import ABC
from dataclasses import dataclass
from enum import Enum
from typing import Collection, ForwardRef, Type, Union

from dacite import Config, from_dict

from pydmx.openfixturelibrary.capabilitySchema import (
    CapabilitySchema,
    ColorIntensity,
    ShutterStrobe,
    Tilt,
)
from pydmx.openfixturelibrary.fixtureSchema import FixtureSchema

data = json.load(open("./test.json"))

test_fixture = from_dict(
    data_class=FixtureSchema, data=data, config=Config(cast=[Enum],),
)
print(test_fixture)

# print([cls.__name__ for cls in CapabilitySchema.__subclasses__()])

import json
from abc import ABC
from dataclasses import dataclass
from enum import Enum
from typing import Collection, ForwardRef, Type, Union

from dacite import Config, from_dict

from pydmx.openfixturelibrary.fixtureSchema import FixtureSchema
from pydmx.openfixturelibrary.capabilitySchema import CapabilitySchema, ColorIntensity, ShutterStrobe, Tilt

data = json.load(open("./test.json"))

test_fixture = from_dict(
    data_class=FixtureSchema,
    data=data,
    config=Config(
      cast=[Enum], 
      forward_references={
        "ShutterStrobe": ShutterStrobe,
        "Tilt": Tilt,
        "ColorIntensity": ColorIntensity
      }
    ),
)
print(test_fixture)

print([cls.__name__ for cls in CapabilitySchema.__subclasses__()])

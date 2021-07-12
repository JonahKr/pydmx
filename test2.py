from dataclasses import dataclass
from enum import Enum
import json
from pydmx.openfixturelibrary.schemaConverter import convert_to_schema

from pydmx.openfixturelibrary.dacite import from_dict, Config

from pydmx.openfixturelibrary.fixtureSchema import FixtureSchema

from typing import Optional, List, Dict

databig = json.load(open("./test.json"))


class Animal(Enum):
    LION = "lion"
    TIGER = "tiger"


@dataclass
class A:
    x: Optional[str]
    y: Optional[Animal]
    z: List[int]


data = {"x": "TEST", "y": "lion", "z": [1, 2, 3]}
print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
#result = from_dict(data_class=A, data=data, config=Config(cast=[Enum]))
# print(result)
print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
result2 = convert_to_schema(A, data)
print(result2)
print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
#result3 = from_dict(data_class=FixtureSchema, data=databig, config=Config(cast=[Enum]))
# print(result3)

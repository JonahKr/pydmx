from dataclasses import dataclass
from enum import Enum
import json
from pydmx.openfixturelibrary.dataclassFactory import create_from_dict

from pydmx.openfixturelibrary.dacite import from_dict, Config

from pydmx.openfixturelibrary.fixtureSchema import FixtureSchema

from typing import Optional, List, Dict

databig = json.load(open("./test.json"))


"""
    "physical": {
        "dimensions": [10,11,12]
    },
"""

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
result = from_dict(data_class=A, data=data, config=Config(cast=[Enum]))
# print(result)
print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
result2 = create_from_dict(A, data)
#print(result2)
print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
#result3 = from_dict(data_class=FixtureSchema, data=databig, config=Config(cast=[Enum]))
#print(result3)

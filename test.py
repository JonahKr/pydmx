import json
from dataclasses import dataclass
from dacite import Config, from_dict
from enum import Enum

json1 = "{}"

class Category(Enum):
  HUMAN = "human"
  ANIMAL = "animal"
  ALIEN = "alien"

@dataclass
class Alive:
  type: Category
  name: str
  height: int

@dataclass
class Human(Alive):
  type = Category.HUMAN
  age: int
  surname: str

@dataclass
class Animal(Alive):
  type = Category.ANIMAL
  species: str

@dataclass
class Alien(Alive):
  type = Category.ALIEN
  planet:str


#ex_alive = '''{"type":"alien", "name":"qlack", "height": 58, "planet":"Mars"}'''
ex_human = '''{"type":"human", "name":"qlack", "height": 58, "planet":"Mars"}'''
ex_animal = '''{"type":"animal", "name":"qlack", "height": 58, "planet":"Mars"}'''
ex_alien = '''{"type":"alien", "name":"qlack", "height": 58, "planet":"Mars"}'''
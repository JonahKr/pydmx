from typing import List, Tuple

from pydmx.fixtureIndex.fixtureIndex import FixtureIndex
from pydmx.openfixturelibrary.fixtureSchema import FixtureSchema

class Fixture(FixtureSchema):

    def __init__(self, fixtureName: str, alias: str, *args, **kwargs):
        # TODO enable path import
        # Linking to Fixture Index
        self.__fixtureIndex = FixtureIndex.getInstance()
        # Importing fixture data from Index
        self.__dict__ = self.__fixtureIndex.lookupFixture(fixtureName).__dict__

    def lookupFixtureName(self, fixtureName: str, *args, **kwargs) -> Tuple[str, str]:
        return ("", "")

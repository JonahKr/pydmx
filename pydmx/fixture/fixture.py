"""
A partial Implementation of the Fixture Schema from: https://github.com/OpenLightingProject/open-fixture-library
Schema Version: 12.2.1
"""

from typing import List, Tuple

from pydmx.fixture.fixtureIndex.fixtureindex import FixtureIndex


class Fixture:
    __fixtureSchemaVersion = "12.2.1"

    def __init__(self, fixtureName: str, alias: str, *args, **kwargs):
        # TODO enable path import
        # Linking to Fixture Index
        self.__fixtureIndex = FixtureIndex.getInstance()
        # Importing fixture data from Index
        fixtDict = self.__fixtureIndex.lookupFixture(fixtureName)

        # ~~~~~~~~~~~~~~~~~
        # Schema Attributes
        # ~~~~~~~~~~~~~~~~~
        # IGNORED ATTRIBUTES: meta, comment, links, helpWanted, rdm, physical, matrix, wheels
        # name: unique in manufacturer
        self.name: str = fixtDict.name
        # shortName: unique in OpenFixtureLibrary
        self.shortName: str = fixtDict.shortName
        # categories:
        self.categories: List[FixtureCategories] = fixtDict.categories
        # matrix
        # wheels
        # List of all the available Channels with their settings for the fixture
        self.availableChannels

    def lookupFixtureName(self, fixtureName: str, *args, **kwargs) -> Tuple[str, str]:
        return ("", "")

import json
import os

from jsonschema import validate

from pydmx.fixtureIndex.dataclassFactory import create_from_dict
from pydmx.openfixturelibrary.fixtureSchema import FixtureSchema

dirname = os.path.dirname(__file__)


class FixtureIndex:
    """
    This Fixture Index (Singleton) is handeling the fixture Library
    """

    __instance = None

    @staticmethod
    def getInstance():
        if FixtureIndex.__instance == None:
            FixtureIndex()
        return FixtureIndex.__instance

    def __init__(self, ofl=True):
        if FixtureIndex.__instance != None:
            raise Exception("Please do not create this Class mulitple times.")
        else:
            FixtureIndex.__instance = self

            self.customfixtures = {}

            self.ofl = None
            if ofl:
                self.ofl = self._loadOfl()

    def _loadOfl(self):
        return json.load(
            open(
                os.path.join(dirname, "./openfixturelibrary/ofl.json"), encoding="utf-8"
            )
        )

    def createCustomFixture(self, fixtureId, fixture):
        # Accepting multiple Filetypes: Json String, Dictionary, and List of the ones before
        instance = None
        if isinstance(fixture, str):
            instance = json.loads(fixture)
        elif isinstance(fixture, dict):
            instance = fixture
        elif isinstance(fixture, list):
            for fixt in fixture:
                self.createCustomFixture(fixt)

        if not self._schema:
            self._schema = open(
                os.path.join(dirname, "./openfixturelibrary/schemas/fixture.json")
            ).read()

        # Validating the Instance with the OFL schema
        try:
            validate(instance=instance, schema=self._schema)
        except:
            return print("The fixture didn't fit the Schema.")

        if fixtureId in self.customfixtures:
            return print("This ID already exists")

        self.customfixtures[fixtureId] = instance

    def removeCustomFixture(self, fixtureId):
        try:
            self.customfixtures.pop(fixtureId)
        except KeyError:
            print("Fixture ID doesn't exist")

    def exportCustomFixtures(self, path, fixtureId=None):
        pass

    def importCustomFixtures(self, path):
        try:
            fixtures = open(path, encoding="utf-8")
        except:
            return print("File doesn't exist")

        for fixtureId, fixture in fixtures.items():
            self.createCustomFixture(fixtureId, fixture)

    def lookupFixture(self, fixtureId: str) -> Type[FixtureSchema]:
        """Looks for Fixture Definitions in CustomDirectory aswell as OFL

        Args:
            fixtureId (str): The id to lookup.

        Returns:
            Type[FixtureSchema]: Object of FixtureSchema or None
        """
        # TODO: FixtureNotFoundError
        fixture = None
        if self.customfixtures and (fixtureId in self.customfixtures):
            fixture = self.customfixtures[fixtureId]
        if self.ofl and (fixtureId in self.ofl):
            fixture = self.ofl[fixtureId]
        return create_from_dict(schema=FixtureSchema, data=fixture)

from pydmx.controller.controller import DMXController
from pydmx.fixture.fixture import Fixture


class Universe:
    def __init__(self):
        self.controller: DMXController = None
        self.buffer = list((0,) * 512)
        self.fixtureRegistry = {}

    def addFixture(self, fixtureName: str, alias: str):
        try:
            fixture = Fixture(fixtureName, alias)
        except:
            print("Sorry, PyDmx was unable to create this Fixture.")

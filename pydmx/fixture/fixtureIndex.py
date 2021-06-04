class FixtureIndex:
    __instance: FixtureIndex = None

    @staticmethod
    def getInstance() -> FixtureIndex:
        if FixtureIndex.__instance == None:
            FixtureIndex()
        return FixtureIndex.__instance

    def __init__(self):
        if FixtureIndex.__instance != None:
            raise Exception("Please do not create this Class mulitple times.")
        else:
            FixtureIndex.__instance = self

    def lookupFixture(self, fixtureName: str):
        pass

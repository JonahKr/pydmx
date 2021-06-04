from pydmx.controller.controller import DMXController


class Universe:
    def __init__(self):
        self.controller: DMXController = None
        self.buffer = list((0,) * 512)

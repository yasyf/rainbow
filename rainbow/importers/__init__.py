from abc import ABCMeta

class Importer(metaclass=ABCMeta):

    def __init__(self):
        self.lines = []

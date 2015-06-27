from abc import ABCMeta, abstractmethod
import rainbow.parser

class Importer(metaclass=ABCMeta):

    def __init__(self):
        self.lines = []

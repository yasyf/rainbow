from abc import ABCMeta, abstractmethod

class Importer(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def foo(self):
        pass

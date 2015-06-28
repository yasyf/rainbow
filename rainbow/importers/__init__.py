from abc import ABCMeta, abstractmethod

class Importer(metaclass=ABCMeta):
    def __init__(self):
        self.data = None

    @abstractmethod
    def open(self, file):
        return self

    def read(self):
        return self.data

    @classmethod
    def get_importer(cls, type_):
        return {
            'google_docs': GoogleDocImporter
        }[type_]

from .google.google_doc_importer import GoogleDocImporter

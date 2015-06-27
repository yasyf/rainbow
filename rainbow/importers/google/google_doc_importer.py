from rainbow.importers import Importer
import re, urllib.request

class GoogleDocImporter(Importer):

    def __init__(self, googleDocUrl):
        super()
        googleDocUrlId = re.search('docs.google.com/document/d/([\w-]+)/', googleDocUrl).group(1)
        self.lines = urllib.request.urlopen("https://docs.google.com/document/export?format=txt&id=" + googleDocUrlId).readlines()

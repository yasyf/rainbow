from rainbow.importers import Importer
import re, requests

class GoogleDocImporter(Importer):

    PATTERN = re.compile(r'd/([\w-]+)/')
    URL = 'https://docs.google.com/document/export?format=txt&id={}'

    def open(self, url):
        match = self.PATTERN.search(url)
        if match:
            document_id = match.group(1)
        else:
            return

        self.data = requests.get(self.URL.format(document_id)).text

        return super().open(url)

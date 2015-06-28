from rainbow.importers import Importer
import re, requests

class GoogleDocImporter(Importer):

    PATTERN = re.compile(r'd/([\w-]+)/')
    URL = 'https://docs.google.com/document/export?format=txt&id={}'
    NO_AUTH_TITLE = '<title>Google Docs - create and edit documents online, for free.</title>'

    def open(self, url):
        match = self.PATTERN.search(url)
        if match:
            document_id = match.group(1)
            data = requests.get(self.URL.format(document_id)).text.strip()
            if self.NO_AUTH_TITLE not in data:
                self.data = data

        return super().open(url)

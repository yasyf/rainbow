from .helpers import monkeypatch

monkeypatch()

import os

dev = os.environ.get('DEV') == 'true'

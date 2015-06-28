from pymongo import MongoClient
import os

client = MongoClient(os.environ.get('MONGOLAB_URI'))
db = client[os.environ.get('MONGOLAB_URI').split('/')[-1]]
calendars = db.calendars
geocache = db.geocache

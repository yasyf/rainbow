from json import JSONEncoder
import datetime, uuid

class RainbowJSONEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        if isinstance(obj, uuid.UUID):
            return str(obj)
        return JSONEncoder.default(self, obj)

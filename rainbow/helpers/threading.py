from multiprocessing import Pool
from rainbow.importers import Importer
from rainbow.models.calendar.calendar import Calendar
from rainbow.parser.parser import parse
from rainbow.web.app import dev


def parse_calendar(type_, file):
    importer = Importer.get_importer(type_)
    data = importer().open(file).read()
    events = parse(data)
    calendar = Calendar(file, events)
    return calendar.save()

class Pooler(object):
    pool = Pool(2)

    @classmethod
    def submit(cls, f, *args):
        if dev:
            return f(*args)
        else:
            return cls.pool.apply_async(f, args)

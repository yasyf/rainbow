from multiprocessing import Pool
import time, os
from rainbow.helpers.location import cache_geolocation_info_for_event
from rainbow.helpers.mongo import calendars
from rainbow.importers import Importer
from rainbow.models.calendar.calendar import Calendar
from rainbow.parser.parser import Parser
from rainbow import dev


def monitor():
    while True:
        for calendar_data in calendars.find({'data': {'$exists': True}}):
            calendar = Calendar.from_pickle(calendar_data['pickle'])
            Pooler.submit(parse_calendar, calendar.type, calendar.url, [None, None], calendar.data)
        time.sleep(int(os.getenv('MONITOR_DELAY') or 30))

def parse_calendar(type_, file, user_geo, existing_data=None):
    print('Processing {}'.format(file))
    importer = Importer.get_importer(type_)
    data = importer().open(file).read()
    if not data:
        Calendar.from_url(file, type_).destroy()
        return
    if data == existing_data:
        return
    events = Parser().parse(data)
    if all(user_geo):
        for event in events:
            if not event.latitude:
                cache_geolocation_info_for_event(event, *user_geo)
    calendar = Calendar(file, type_, data, events)
    return calendar.save()


class Pooler(object):
    pool = Pool(2)

    @classmethod
    def submit(cls, f, *args):
        if dev:
            return f(*args)
        else:
            return cls.pool.apply_async(f, args)

if __name__ == '__main__':
    monitor()

from operator import methodcaller
import icalendar, pickle, bson
from rainbow.helpers.mongo import calendars


class Calendar(object):
    VERSION = 1.0

    def __init__(self, url: str, type: str, data: str, events):
        self.prodid = '-//{}//{}//'.format(self.__class__.__name__, self.__class__.__module__)
        self.url = url
        self.type = type
        self.data = data
        self.events = events

    def to_ical(self):
        cal = icalendar.Calendar()
        cal.add('prodid', self.prodid)
        cal.add('version', self.VERSION)
        cal.add('summary', self.url)
        list(map(cal.add_component, map(methodcaller('to_ical'), self.events)))
        return cal.to_ical()

    def to_dict(self):
        return {'events': list(map(methodcaller('to_dict'), self.events))}

    @classmethod
    def _find_by_url(cls, url):
        return calendars.find_one({'url': url})

    @classmethod
    def _find_by_id(cls, _id):
        return calendars.find_one({'_id': bson.ObjectId(_id)})

    def _serialize(self):
        return {
            'type': self.type,
            'data': self.data,
            'url': self.url,
            'pickle': pickle.dumps(self)
        }

    @classmethod
    def id_from_url(cls, url):
        found = cls._find_by_url(url)
        if found:
            return found['_id']

    @classmethod
    def find(cls, _id):
        if _id == 'demo':
            return CalendarFixture.get()
        found = cls._find_by_id(_id)
        if found:
            return pickle.loads(found['pickle'])

    @classmethod
    def from_pickle(cls, picked):
        return pickle.loads(picked)

    @classmethod
    def from_url(cls, url):
        found = cls._find_by_url(url)
        if found:
            return cls.from_pickle(found['pickle'])
        else:
            return cls(url, None, None, [])

    def save(self):
        found = self._find_by_url(self.url)
        if found:
            _id = found['_id']
            calendars.update({'_id': _id}, self._serialize())
            return _id
        return calendars.insert(self._serialize())

from rainbow.fixtures.calendar_fixture import CalendarFixture

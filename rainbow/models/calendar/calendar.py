import icalendar
from rainbow.models.event import Event


class Calendar(object):
    VERSION = 1.0

    def __init__(self, events):
        self.prodid = '-//{}//{}//'.format(self.__class__.__name__, self.__class__.__module__)
        self.events = events

    def to_ical(self):
        cal = icalendar.Calendar()
        cal.add('prodid', self.prodid)
        cal.add('version', self.VERSION)
        list(map(cal.add_component, map(Event.to_ical, self.events)))
        return cal.to_ical()

    def to_dict(self):
        return {
            'events': list(map(Event.to_dict, self.events))
        }

    @classmethod
    def find(cls, id):
        if id == 'demo':
            return CalendarFixture.get()

from rainbow.fixtures.calendar_fixture import CalendarFixture

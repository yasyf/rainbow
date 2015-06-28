import datetime, uuid
from abc import ABCMeta, abstractmethod
import icalendar, dateutil.rrule

class Event(object, metaclass=ABCMeta):
    def __init__(self, group_id: uuid.UUID=None, title: str=None, description: str=None,
                location: str=None, website: str=None, start_date: datetime.date=None,
                end_date: datetime.date=None, start_time: datetime.time=None,
                end_time: datetime.time=None, **kwargs):
        self.group_id = group_id or uuid.uuid4()
        self.title = title
        self.description = description
        self.website = website
        self.start_date = start_date or datetime.date.today()
        self.end_date = end_date
        self.location = location
        self.start_time = start_time or datetime.time()
        self.end_time = end_time
        try:
            self.check_assertions()
        except AssertionError as e:
            raise EventError(e.args[0]) from e

    @property
    def latitude(self) -> float:
        return None

    @property
    def longitude(self) -> float:
        return None

    @abstractmethod
    def rrule(self) -> icalendar.vRecur:
        return None

    def to_dict(self):
        return {
            'group_id': self.group_id,
            'title': self.title,
            'description': self.description,
            'location': {
                'value': self.location,
                'latitude': self.latitude,
                'longitude': self.longitude,
            },
            'rrule': self.rrule().to_ical().decode() if self.rrule() else None,
            'start': datetime.datetime.combine(self.start_date, self.start_time),
            'end': datetime.datetime.combine(self.end_date or self.start_date,
                                             self.end_date or self.start_time)
                                            if self.end_date or self.end_time
                                            else None
        }

    def to_ical(self) -> icalendar.Event:
        event = icalendar.Event()
        event.add('uid', self.group_id)
        event.add('summary', self.title)
        for field in ['description', 'location']:
            if getattr(self, field):
                event.add(field, getattr(self, field))
        rrule = self.rrule()
        if rrule:
            event.add('rrule', rrule)
        start = datetime.datetime.combine(self.start_date, self.start_time)
        event.add('dtstart', start)
        if self.end_date or self.end_time:
            end = datetime.datetime.combine(self.end_date or self.start_date,
                                            self.end_time or self.start_time)
            event.add('dtend', end)
        return event

    @abstractmethod
    def check_assertions(self):
        assert self.title is not None
        assert isinstance(self.group_id, uuid.UUID)
        assert isinstance(self.start_date, datetime.date)
        assert isinstance(self.start_time, datetime.time)
        if self.end_time:
            assert isinstance(self.end_time, datetime.time)

    @abstractmethod
    def is_on_date(self, date: datetime.date) -> bool:
        if date < self.start_date:
            return False
        return True

    def is_on_day_of_month(self, day: int, month: int) -> bool:
        return self.is_on_date(datetime.date.today().replace(day=day, month=month))

class EventError(RuntimeError):
    pass

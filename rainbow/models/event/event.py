import datetime, uuid
from abc import ABCMeta, abstractmethod

class Event(object, metaclass=ABCMeta):
    def __init__(self, group_id: uuid.UUID = None, title: str = None, description: str = None,
                location: str = None, website: str = None, start_date: datetime.date = None,
                time: datetime.time = None, **kwargs):
        self.group_id = group_id or uuid.uuid4()
        self.title = title
        self.description = description
        self.website = website
        self.start_date = start_date or datetime.date.today()
        self.location = location
        self.time = time
        try:
            self.check_assertions()
        except AssertionError as e:
            raise EventError(e.args[0]) from e

    @property
    def latitude(self):
        return None

    @property
    def longitude(self):
        return None

    @abstractmethod
    def check_assertions(self):
        assert self.title is not None
        assert isinstance(self.group_id, uuid.UUID)
        assert isinstance(self.start_date, datetime.date)
        if self.time:
            assert isinstance(self.time, datetime.time)

    @abstractmethod
    def is_on_date(self, date: datetime.date) -> bool:
        if date < self.start_date:
            return False
        return True

    def is_on_day_of_month(self, day: int, month: int) -> bool:
        return self.is_on_date(datetime.date.today().replace(day=day, month=month))

class EventError(RuntimeError):
    pass

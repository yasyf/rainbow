import datetime, uuid
from abc import ABCMeta, abstractmethod

class Event(metaclass=ABCMeta):
    def __init__(self, group_id: uuid.UUID, title: str, description: str,
                website: str, start_date: datetime.date, time: datetime.time):
        self.group_id = group_id
        self.title = title
        self.description = description
        self.website = website
        self.start_date = start_date
        self.time = time
        try:
            self.check_assertions()
        except AssertionError as e:
            raise EventError(e.args[0]) from e

    @abstractmethod
    def check_assertions(self):
        pass

    @abstractmethod
    def is_on_date(self, date: datetime.date) -> bool:
        if date < self.start_date:
            return False
        return True

    def is_on_day_of_month(self, day: int, month: int) -> bool:
        return self.is_on_date(datetime.date.today().replace(day=day, month=month))

class EventError(RuntimeError):
    pass

import datetime
from .event import Event
from ...enums.month import Month

class OneTimeEvent(Event):
    def __init__(self, day: int, month: Month, **kwargs):
        self.day = day
        self.month = month
        super().__init__(**kwargs)

    def check_assertions(self):
        assert 1 <= self.day <= 31, "invalid day"
        assert 1 <= self.month <= 12, "invalid month"

    def is_on_date(self, date: datetime.date) -> bool:
        return date.day == self.day and date.month == self.month

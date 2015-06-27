import datetime
from .event import Event

class MonthlyEvent(Event):
    def __init__(self, day: int, **kwargs):
        self.day = day
        super().__init__(**kwargs)

    def check_assertions(self):
        assert 0 <= self.day <= 31, "invalid day"

    def is_on_date(self, date: datetime.date) -> bool:
        return date.day == self.day

import datetime
from .event import Event

class OneTimeEvent(Event):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def date(self):
        return self.start_date

    @date.setter
    def date(self, date):
        self.start_date = date

    def is_on_date(self, date: datetime.date) -> bool:
        if not super().is_on_date(date):
            return False
        return date.day == self.date

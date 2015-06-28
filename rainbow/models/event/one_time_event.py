import datetime
from .event import Event

class OneTimeEvent(Event):
    def __init__(self, date: datetime.date=None, **kwargs):
        kwargs['start_date'] = date
        super().__init__(**kwargs)

    def check_assertions(self):
        super().check_assertions()

    @property
    def date(self):
        return self.start_date

    @date.setter
    def date(self, date):
        self.start_date = date

    def rrule(self):
        return None

    def is_on_date(self, date: datetime.date) -> bool:
        if not super().is_on_date(date):
            return False
        return date == self.date

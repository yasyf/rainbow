from abc import ABCMeta
import datetime
from rainbow.models.event.event import Event

class MonthlyEvent(Event, metaclass=ABCMeta):
    def __init__(self, skip_months: int, **kwargs):
        self.skip_months = skip_months
        super().__init__(**kwargs)

    def check_assertions(self):
        assert 1 <= self.skip_months <= 12, "invalid skip_months"

    def is_on_date(self, date: datetime.date) -> bool:
        if not super().is_on_date(date):
            return False
        months_skipped = date.month - self.start_date.month
        return (months_skipped % self.skip_months) == 0

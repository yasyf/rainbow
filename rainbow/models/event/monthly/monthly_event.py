from abc import ABCMeta
import datetime
from rainbow.models.event.event import Event

class MonthlyEvent(Event, metaclass=ABCMeta):
    def __init__(self, skip_months: int=None, **kwargs):
        self.skip_months = skip_months
        super().__init__(**kwargs)

    def check_assertions(self):
        super().check_assertions()
        assert 0 <= self.skip_months <= 11, "invalid skip_months ({})".format(self.skip_months)

    def is_on_date(self, date: datetime.date) -> bool:
        if not super().is_on_date(date):
            return False
        if self.skip_months == 0:
            return True
        months_skipped = date.month - self.start_date.month
        if months_skipped == 0:
            return True
        return (months_skipped % (self.skip_months + 1)) == 0

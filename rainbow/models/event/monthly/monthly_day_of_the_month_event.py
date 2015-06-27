import datetime
from rainbow.models.event import MonthlyEvent


class MonthlyDayOfTheMonthEvent(MonthlyEvent):
    def __init__(self, date: int, **kwargs):
        self.date = date
        super().__init__(**kwargs)

    def check_assertions(self):
        super().check_assertions()
        assert 1 <= self.date <= 31, "invalid date"

    def is_on_date(self, date: datetime.date) -> bool:
        if not super().is_on_date(date):
            return False
        return date.day == self.date


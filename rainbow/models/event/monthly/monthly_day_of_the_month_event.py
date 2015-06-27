import datetime
from rainbow.models.event import MonthlyEvent


class MonthlyDayOfTheWeekEvent(MonthlyEvent):
    def __int__(self, date: int):
        self.date = date

    def check_assertions(self):
        assert 1 <= self.date <= 31, "invalid date"

    def is_on_date(self, date: datetime.date) -> bool:
        if not super().is_on_date(date):
            return False
        return date.day == self.date


import datetime
from rainbow.enums.day_of_the_week import DayOfTheWeek
from rainbow.helpers.dates import week_of_the_month
from rainbow.models.event import MonthlyEvent


class MonthlyDayOfTheWeekEvent(MonthlyEvent):
    def __int__(self, day_of_the_week: DayOfTheWeek, week: int):
        self.day_of_the_week = day_of_the_week
        self.week = week

    def check_assertions(self):
        assert 0 <= self.day_of_the_week <= 6, "invalid DayOfTheWeek"
        assert 1 <= self.week <= 5, "invalid week"

    def is_on_date(self, date: datetime.date) -> bool:
        if not super().is_on_date(date):
            return False
        if date.weekday() != self.day_of_the_week:
            return False
        return self.week == week_of_the_month(date)


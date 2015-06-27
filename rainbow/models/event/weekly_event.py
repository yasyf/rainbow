import datetime
from .event import Event
from ...enums.day_of_the_week import DayOfTheWeek


class WeeklyEvent(Event):
    def __init__(self, day_of_the_week: DayOfTheWeek, skip_weeks: int, **kwargs):
        self.day_of_the_week = day_of_the_week
        self.skip_weeks = skip_weeks
        super().__init__(**kwargs)

    def check_assertions(self):
        assert 0 <= self.day_of_the_week <= 6, "invalid DayOfTheWeek"

    def is_on_date(self, date: datetime.date) -> bool:
        if not super().is_on_date(date):
            return False
        if date.weekday() != self.day_of_the_week:
            return False
        weeks_skipped = (date - self.start_date).days // 7
        return (weeks_skipped % self.skip_weeks) == 0

import datetime
from .event import Event
from ...enums.day_of_the_week import DayOfTheWeek


class WeeklyEvent(Event):
    def __init__(self, day_of_the_week: DayOfTheWeek, **kwargs):
        self.day_of_the_week = day_of_the_week
        super().__init__(**kwargs)

    def check_assertions(self):
        assert 0 <= self.day_of_the_week <= 6, "invalid DayOfTheWeek"

    def is_on_date(self, date: datetime.date) -> bool:
        return date.weekday() == self.day_of_the_week

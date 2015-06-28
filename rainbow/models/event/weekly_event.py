import datetime
import dateutil.rrule
import icalendar
from .event import Event
from ...enums.day_of_the_week import DayOfTheWeek


class WeeklyEvent(Event):
    def __init__(self, day_of_the_week: DayOfTheWeek, skip_weeks: int, **kwargs):
        self.day_of_the_week = day_of_the_week
        self.skip_weeks = skip_weeks
        super().__init__(**kwargs)

    def check_assertions(self):
        super().check_assertions()
        assert 0 <= self.day_of_the_week <= 6, "invalid DayOfTheWeek"
        assert 0 <= self.skip_weeks <= 51, "invalid skip_weeks"

    def is_on_date(self, date: datetime.date) -> bool:
        if not super().is_on_date(date):
            return False
        if date.weekday() != self.day_of_the_week:
            return False
        if self.skip_weeks == 0:
            return True
        weeks_skipped = (date - self.start_date).days // 7
        if weeks_skipped == 0:
            return True
        return (weeks_skipped % (self.skip_weeks + 1)) == 0

    def rrule(self):
        byday = dateutil.rrule.weekday(self.day_of_the_week)
        return icalendar.vRecur(freq='weekly', interval=self.skip_weeks + 1,
                                byday=byday)

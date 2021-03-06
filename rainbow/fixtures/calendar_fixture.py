import datetime
from rainbow.enums.day_of_the_week import DayOfTheWeek
from rainbow.models.event import OneTimeEvent, WeeklyEvent
from rainbow.models.event.monthly.monthly_day_of_the_month_event import MonthlyDayOfTheMonthEvent
from rainbow.models.event.monthly.monthly_day_of_the_week_event import MonthlyDayOfTheWeekEvent

class CalendarFixture(object):
    @staticmethod
    def get():
        june = datetime.date(2015, month=6, day=1)
        tomorrow = datetime.date(2015, month=6, day=28)
        events = [
            MonthlyDayOfTheWeekEvent(title='foo', start_date=june, skip_months=0,
                                     day_of_the_week=DayOfTheWeek.monday, week=1),
            MonthlyDayOfTheMonthEvent(title='foo', start_date=june, skip_months=0, date=1),
            OneTimeEvent(title='foo', date=tomorrow),
            WeeklyEvent(title='foo', start_date=june,
                        day_of_the_week=DayOfTheWeek.monday, skip_weeks=0)

        ]
        return Calendar('demo', 'google_docs', '', events)

from rainbow.models.calendar.calendar import Calendar

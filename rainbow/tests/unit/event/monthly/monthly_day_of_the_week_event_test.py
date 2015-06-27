import unittest, datetime
from rainbow.enums.day_of_the_week import DayOfTheWeek
from rainbow.models.event.monthly.monthly_day_of_the_week_event import MonthlyDayOfTheWeekEvent


class MonthlyDayOfTheWeekEventTest(unittest.TestCase):
    def setUp(self):
        self.june = datetime.date(2015, month=6, day=1)
        self.event = MonthlyDayOfTheWeekEvent(title='foo', start_date=self.june, skip_months=0,
                                                day_of_the_week=DayOfTheWeek.monday, week=1)

    def test_is_on_date_no_skip(self):
        self.assertTrue(self.event.is_on_date(self.june.replace(day=1)))
        self.assertFalse(self.event.is_on_date(self.june.replace(day=8)))
        self.assertFalse(self.event.is_on_date(self.june.replace(day=15)))
        self.assertTrue(self.event.is_on_date(self.june.replace(month=7, day=6)))

    def test_is_on_date_with_skip_1(self):
        self.event.skip_months = 1
        self.assertTrue(self.event.is_on_date(self.june.replace(day=1)))
        self.assertFalse(self.event.is_on_date(self.june.replace(month=7, day=6)))
        self.assertTrue(self.event.is_on_date(self.june.replace(month=8, day=3)))


if __name__ == '__main__':
    unittest.main()

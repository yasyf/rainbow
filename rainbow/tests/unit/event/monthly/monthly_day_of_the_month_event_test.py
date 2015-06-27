import unittest, datetime
from rainbow.models.event.monthly.monthly_day_of_the_month_event import MonthlyDayOfTheMonthEvent


class MonthlyDayOfTheMonthEventTest(unittest.TestCase):
    def setUp(self):
        self.june = datetime.date(2015, month=6, day=1)
        self.event = MonthlyDayOfTheMonthEvent(title='foo', start_date=self.june, skip_months=0,
                                                date=1)

    def test_is_on_date_no_skip(self):
        self.assertTrue(self.event.is_on_date(self.june.replace(day=1)))
        self.assertFalse(self.event.is_on_date(self.june.replace(day=8)))
        self.assertTrue(self.event.is_on_date(self.june.replace(month=7, day=1)))

    def test_is_on_date_with_skip_1(self):
        self.event.skip_months = 1
        self.assertTrue(self.event.is_on_date(self.june.replace(day=1)))
        self.assertFalse(self.event.is_on_date(self.june.replace(month=7, day=1)))
        self.assertTrue(self.event.is_on_date(self.june.replace(month=8, day=1)))


if __name__ == '__main__':
    unittest.main()

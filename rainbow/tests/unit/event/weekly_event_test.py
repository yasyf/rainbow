import unittest, datetime
from rainbow.enums.day_of_the_week import DayOfTheWeek
from rainbow.models.event import WeeklyEvent


class WeeklyEventTest(unittest.TestCase):
    def setUp(self):
        self.june = datetime.date(2015, month=6, day=1)
        self.event = WeeklyEvent(title='foo', start_date=self.june,
                                 day_of_the_week=DayOfTheWeek.monday, skip_weeks=0)

    def test_is_on_date_no_skip(self):
        self.assertTrue(self.event.is_on_date(self.june.replace(day=1)))
        self.assertTrue(self.event.is_on_date(self.june.replace(day=8)))
        self.assertTrue(self.event.is_on_date(self.june.replace(day=15)))

    def test_is_on_date_with_skip_1(self):
        self.event.skip_weeks = 1
        self.assertTrue(self.event.is_on_date(self.june.replace(day=1)))
        self.assertFalse(self.event.is_on_date(self.june.replace(day=8)))
        self.assertTrue(self.event.is_on_date(self.june.replace(day=15)))

    def test_is_on_date_with_skip_3(self):
        self.event.skip_weeks = 3
        self.assertTrue(self.event.is_on_date(self.june.replace(day=1)))
        self.assertFalse(self.event.is_on_date(self.june.replace(day=8)))
        self.assertFalse(self.event.is_on_date(self.june.replace(day=15)))
        self.assertFalse(self.event.is_on_date(self.june.replace(day=22)))
        self.assertTrue(self.event.is_on_date(self.june.replace(day=29)))

if __name__ == '__main__':
    unittest.main()

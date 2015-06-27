import unittest, datetime
from rainbow.models.event import OneTimeEvent


class OneTimeEventTest(unittest.TestCase):
    def test_is_on_date(self):
        tomorrow = datetime.date(2015, month=6, day=28)
        event = OneTimeEvent(title='foo', date=tomorrow)
        self.assertTrue(event.is_on_date(tomorrow))
        self.assertFalse(event.is_on_date(tomorrow + datetime.timedelta(days=1)))

if __name__ == '__main__':
    unittest.main()

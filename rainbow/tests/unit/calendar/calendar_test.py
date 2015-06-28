import unittest
from rainbow.fixtures.calendar_fixture import CalendarFixture


class CalendarTest(unittest.TestCase):
    def setUp(self):
        self.calendar = CalendarFixture.get()

    def test_to_ical(self):
        ical = self.calendar.to_ical().decode()
        self.assertIn('BEGIN:VCALENDAR', ical)
        self.assertEqual(714, len(ical))

if __name__ == '__main__':
    unittest.main()

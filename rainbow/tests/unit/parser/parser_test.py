import unittest, datetime
from rainbow.models.event.monthly.monthly_day_of_the_week_event import MonthlyDayOfTheWeekEvent
from rainbow.models.event.weekly_event import WeeklyEvent
from rainbow.models.event.one_time_event import OneTimeEvent
from rainbow.parser.parser import Parser

class ParserTest(unittest.TestCase):
    def test_parser(self):
        trial = """May 30: Treasure Island Flea Market (also last weekend of every month)
June 4: SF Design Week
June 6 : Union Street Festival
June 13 : Bubble Battle
June 13 : North Beach Festival
June 14 : Haight Ashbury Street Fair
June 18 : LGBTQ Film Festival
June 20 : Fantastic Mr. Fox Showing on Fieldee Outside
June 25 : Internapalooza
June 26: Trans March
June 26 : Post - Giants Fireworks Show
June 27 : LGBT Pride Parade
July 4 : Fourth of July Celebration on the Pier
July 4 : Fillmore Jazz Festival
July 11 : Salsa Festival (free lessons!)
July 17: Renegade Craft Fair
July 17: Frozen Film Festival
July 18 : Poochella
July 25 : Manchester and Barcelona game
July 26 : SF Half Marathon
July 31: American Craft Council Craft Show
August 1 : Vintage Paper Fair
August 7 : Outside Lands
August 15 : SF Street Food Festival
August 20 : Eat Drink SF
August 23 : The Giant Race Half Marathon"""
        p = Parser()
        parsed = p.parse(trial)
        self.assertIsInstance(parsed, list)
        for i in range(len(trial.split('\n'))-1):
            self.assertIsInstance(parsed[i], OneTimeEvent)

    def test_times(self):
        trial = """every Friday at 4pm: SF Design Week"""
        p = Parser()
        parsed = p.parse(trial)
        self.assertIsInstance(parsed[0],WeeklyEvent)
        self.assertEquals(parsed[0].to_dict()['start'].time(),datetime.time(16))

if __name__ == '__main__':
    unittest.main()

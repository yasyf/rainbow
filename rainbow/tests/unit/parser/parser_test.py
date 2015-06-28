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

    def test_demo(self):
        trial = """
        6/5 Reserve for Diego Rivera Mural Tour! (the tour is on 6/15 but need to reserve 10 days in advance, 25 person cap)


Events with Specific Dates
May 30 : Treasure Island Flea Market (also last weekend of every month)
June 4 : SF Design Week
June 6  : Union Street Festival
June 13 : Bubble Battle
June 13  : North Beach Festival
June 14 : Haight Ashbury Street Fair
June 18 : LGBTQ Film Festival
June 20 : Fantastic Mr. Fox Showing on Fieldee Outside
June 25 : Internapalooza
June 26: Trans March
June 26 : Post - Giants Fireworks Show
June 27 - 28 : LGBT Pride Parade
July 4 : Fourth of July Celebration on the Pier
July 4  : Fillmore Jazz Festival
July 11 : Salsa Festival (free lessons!)
July 17 : Renegade Craft Fair
July 17 : Frozen Film Festival
July 18 : Poochella
July 25 : Manchester and Barcelona game
July 26 : SF Half Marathon
July 31  : American Craft Council Craft Show
August 1  : Vintage Paper Fair
August 7  : Outside Lands
August 15  : SF Street Food Festival
August 20 : Eat Drink SF
August 23 : The Giant Race Half Marathon


General Locations
* Walk across Golden Gate Bridge
* Chill in Golden Gate Park (Hippie Drum Circle + Oldest Japanese Tea Garden)
* Cable car ride
* Alcatraz
* Giants Baseball game (June 15, 16 are vs. Mariners, home)
* Exploratorium
* Musee Mecanique
* Sea Lions at Pier 39 + other attractions
* Yosemite
* Hike Grizzly Peak
* Seward Mini Park Slides
* Bernal Heights Night Picnic
* Gain the courage to bike down Filbert Street
* Angel Island
* Climb Coit Tower
* Urban Putt Miniature Golf?
* Twin Peaks View
* Ghirardelli Square
* Billy Goat Hill Rope Swing
	Recurring Events
* Ferry Building Marketplace, Tuesdays, Thursdays, and Saturdays until 2pm
* Free first weekend of every month, Museums (w/ Bank of America)
* Last weekend of every month, Treasure Island Flea Market
* Free first Tuesday of every month, de Young Museum + Conservatory of Flowers + Museum of Craft and Design
* Free first Wednesday of every month, Comedy and Hot Dogs + Comedy + Comedy
* Free Thursdays, Twilight on the Presidio, NightLife!!!!!
* First Thursdays, Exploratorium After Dark
* Free second Tuesday of every month, SF Botanical Garden (always free for residents)
* Free third Thursday of every month, Full Frontal Comedy
* Free first Friday of every month, North Beach Art Crawl + SF Bike Party
* Free second and fourth Friday of every month, Coffee
* Free last Friday of every month, Critical Mass Bike Ride
* Fourth Friday of every month, Union Square Dancing
* Every Friday and Saturday, Audium “Blow your mind”
* First Saturday of every month, Michael Jackson and Prince Dance Party
* Second Saturday of every month, $1 Book Sale + Free Sexy Comedy and Pizza
* Third Saturday of every month, New Wave Dance Party
* Free third Saturday of every month, Mystery Midnight Ride + Morrissey and the Smiths Dance Party
* Free Sundays at 1 PM, Golden Gate Park Band
* Free Sundays at 2 PM, Stern Grove Music Festival Concerts
* Free Sundays, Picnic at the Presidio + Alemany Flea Market
* Free first Sunday of every month, Hot Dogs
* 6/10 and 7/8, Haters Gonna Hate Comedy Show
* Romeo and Juliet performance


Art
* Caruso’s Dream
* 16th avenue tiled steps
* 18th and Castro rainbow sidewalks


Notes
* On Sundays, main road through Golden Gate Park is closed so people can wander freely
* Some of these events are 21+ only :(








Food


$
Golden Gate Fortune Cookie Company (Chinatown)
The Flying Falafel (SoMa)
Lou’s Cafe (Inner Richmond)
The Codmother Fish and Chips (FIsherman’s Wharf)
El Farolito (Mission)


$$
The Tonga Room (Union)
The Italian Homemade Company (North Beach)
Ike’s Place (Castro)
Burma Superstar (Inner Richmond)
San Tung Chinese Restaurant (Inner Sunset)
Hog Island Oyster Co (SoMa)
Tartine (Mission)


$$$
Yank Sing Dimsum (SoMa)
Cliff House (Sutro Baths)
Foreign Cinema (Mission)
John’s Grill (SoMA) -- In The Maltese Falcon
Kokkari Estiatorio (FiDi)
NoPa (Alamo Square)


$$$$
Gary Danko (Fisherman’s Wharf)

"""
        p = Parser()
        parsed = p.parse(trial)
        self.assertIsInstance(parsed,list)

if __name__ == '__main__':
    unittest.main()

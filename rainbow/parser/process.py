import nltk
import string
from recurrent import RecurringEvent
import datetime
from rainbow.enums.day_of_the_week import DayOfTheWeek
from rainbow.models.event import WeeklyEvent
from rainbow.models.event.monthly.monthly_day_of_the_month_event import MonthlyDayOfTheMonthEvent
from rainbow.models.event.monthly.monthly_day_of_the_week_event import MonthlyDayOfTheWeekEvent
import uuid

model = {
    'Free': 'IGNORE',
    'FREE': 'IGNORE',
    'free': 'IGNORE',
    'Last': 'IGNORE',
    'last': 'IGNORE',
    'LAST': 'IGNORE',
    'First': 'IGNORE',
    'first': 'IGNORE',
    'FIRST': 'IGNORE',
    'monday': 'IGNORE',
    'tuesday': 'IGNORE',
    'wednesday': 'IGNORE',
    'thursday': 'IGNORE',
    'friday': 'IGNORE',
    'saturday': 'IGNORE',
    'sunday': 'IGNORE',
    'weekend': 'IGNORE',
    'next': 'IGNORE',
    'Next': 'IGNORE',
    'NEXT': 'IGNORE',
    'Monday': 'IGNORE',
    'Tuesday': 'IGNORE',
    'Wednesday': 'IGNORE',
    'Thursday': 'IGNORE',
    'Friday': 'IGNORE',
    'Saturday': 'IGNORE',
    'Sunday': 'IGNORE',
    'mondays': 'IGNORE',
    'tuesdays': 'IGNORE',
    'wednesdays': 'IGNORE',
    'thursdays': 'IGNORE',
    'fridays': 'IGNORE',
    'saturdays': 'IGNORE',
    'sundays': 'IGNORE',
    'weekends': 'IGNORE',
    'next': 'IGNORE',
    'Next': 'IGNORE',
    'NEXT': 'IGNORE',
    'Mondays': 'IGNORE',
    'Tuesdays': 'IGNORE',
    'Wednesdays': 'IGNORE',
    'Thursdays': 'IGNORE',
    'Fridays': 'IGNORE',
    'Saturdays': 'IGNORE',
    'Sundays': 'IGNORE',
    'Weekends': 'IGNORE',
    'month': 'IGNORE',
    'Month': 'IGNORE',
    'PM': 'IGNORE',
    'pm': 'IGNORE',
    'AM': 'IGNORE',
    'am': 'IGNORE',
    '/': 'SLASH',
    'jan': 'MONTH',
    'january': 'MONTH',
    'feb': 'MONTH',
    'february': 'MONTH',
    'mar': 'MONTH',
    'march': 'MONTH',
    'apr': 'MONTH',
    'april': 'MONTH',
    'may': 'MONTH',
    'jun': 'MONTH',
    'june': 'MONTH',
    'jul': 'MONTH',
    'july': 'MONTH',
    'aug': 'MONTH',
    'august': 'MONTH',
    'sep': 'MONTH',
    'september': 'MONTH',
    'oct': 'MONTH',
    'october': 'MONTH',
    'nov': 'MONTH',
    'november': 'MONTH',
    'dec': 'MONTH',
    'december': 'MONTH',
    'Jan': 'MONTH',
    'January': 'MONTH',
    'Feb': 'MONTH',
    'February': 'MONTH',
    'Mar': 'MONTH',
    'March': 'MONTH',
    'Apr': 'MONTH',
    'April': 'MONTH',
    'May': 'MONTH',
    'Jun': 'MONTH',
    'June': 'MONTH',
    'Jul': 'MONTH',
    'July': 'MONTH',
    'Aug': 'MONTH',
    'August': 'MONTH',
    'Sep': 'MONTH',
    'September': 'MONTH',
    'Oct': 'MONTH',
    'October': 'MONTH',
    'Nov': 'MONTH',
    'November': 'MONTH',
    'Dec': 'MONTH',
    'December': 'MONTH',
    'JAN': 'MONTH',
    'JANUARY': 'MONTH',
    'FEB': 'MONTH',
    'FEBRUARY': 'MONTH',
    'MAR': 'MONTH',
    'MARCH': 'MONTH',
    'APR': 'MONTH',
    'APRIL': 'MONTH',
    'MAY': 'MONTH',
    'JUN': 'MONTH',
    'JUNE': 'MONTH',
    'JUL': 'MONTH',
    'JULY': 'MONTH',
    'AUG': 'MONTH',
    'AUGUST': 'MONTH',
    'SEP': 'MONTH',
    'SEPTEMBER': 'MONTH',
    'OCT': 'MONTH',
    'OCTOBER': 'MONTH',
    'NOV': 'MONTH',
    'NOVEMBER': 'MONTH',
    'DEC': 'MONTH',
    'DECEMBER': 'MONTH',
    'of': 'OF',
    'OF': 'OF',
    'Of': 'OF'
}

def process(sentence, chunker):
    sentence = sentence.replace('/', ' / ')
    tokens = nltk.word_tokenize(sentence)
    default_tagger = nltk.data.load(nltk.tag._POS_TAGGER)
    tagger = nltk.tag.UnigramTagger(model=model, backoff=default_tagger)
    tagged = tagger.tag(tokens)
    result = chunker.parse(tagged)
    return result

def one_time_process(date):
    table = str.maketrans("", "", string.punctuation)
    date_string = ' '.join(date).translate(table)
    r = RecurringEvent(now_date=datetime.datetime.utcnow())
    return r.parse(date_string)

def contains_date(event):
    r = RecurringEvent(now_date=datetime.datetime.utcnow())
    try:
        return r.parse(event) is not None
    except ValueError:
        return False

def is_recurring(event):
    r = RecurringEvent(now_date=datetime.datetime.utcnow())
    try:
        r.parse(event)
        return r.is_recurring
    except ValueError:
        return False

def non_recurrent_parse(event):
    r = RecurringEvent(now_date=datetime.datetime.utcnow())
    return r.parse(event)

def recurrent_parse(event):
    r = RecurringEvent(now_date=datetime.datetime.utcnow())
    r.parse(event)
    start_time, success = parse_time(event)
    if success:
        return r, {'start_time':start_time}
    else:
        return r, {}

def recurrent_process(event, title, extra):
    events = []
    params = event.get_params()
    start_time = extra.get('start_time')

    if 'freq' not in params:
        return events

    if params['freq'] == 'yearly':
        return events
    elif params['freq'] == 'weekly':
        days = params['byday'].split(',')
        group = uuid.uuid4()
        for day in days:
            if len(day) == 3:
                day = day[1:]
            events.append(WeeklyEvent(group_id=group, day_of_the_week=DayOfTheWeek[day], skip_weeks=params['interval'] - 1, title=title, start_time=start_time))
    else:
        if 'byday' in params:
            for day in params['byday'].split(','):
                if len(day) == 3:
                    day = day[1:]
                    week = int(day[0])
                else:
                    week = 1
                events.append(MonthlyDayOfTheWeekEvent(skip_months=int(params['interval']) - 1, day_of_the_week=DayOfTheWeek[day], week=week, title=title, start_time=start_time))
        else:
            events.append(MonthlyDayOfTheMonthEvent(skip_months=int(params['interval']) - 1, date=int(params['bymonthday']), title=title, start_time=start_time))
    return events

def parse_time(event):
    dt = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    r = RecurringEvent(now_date=dt)
    start_date, success = r.parse_time(event, dt)
    return start_date.time(), success

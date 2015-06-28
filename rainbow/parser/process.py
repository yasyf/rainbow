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
    if r.parse(event) is None:
        return False
    return True

def is_recurring(event):
    r = RecurringEvent(now_date=datetime.datetime.utcnow())
    r.parse(event)
    if r.is_recurring:
        return True
    return False

def non_recurrent_parse(event):
    r = RecurringEvent(now_date=datetime.datetime.utcnow())
    return r.parse(event)

def recurrent_parse(event):
    r = RecurringEvent(now_date=datetime.datetime.utcnow())
    r.parse(event)
    return r

def recurrent_process(event, title):
    events = []
    params = event.get_params()
    if params['freq'] == 'weekly':
        days = params['byday'].split(',')
        group = uuid.uuid4()
        for day in days:
            events.append(WeeklyEvent(group_id = group, day_of_the_week = DayOfTheWeek[day], skip_weeks = params['interval']-1, title = title))
    else:
        if 'byday' in params:
            if len(params['byday']) == 3:
                day = params['byday'][1:3]
                week = int(params['byday'][0])
            else:
                day = params['byday']
                week = 1
            events.append(MonthlyDayOfTheWeekEvent(skip_months = int(params['interval'])-1, day_of_the_week = DayOfTheWeek[day], week = week, title = title))
        else:
            events.append(MonthlyDayOfTheMonthEvent(skip_months = int(params['interval'])-1, date = int(params['bymonthday']), title = title))
    return events

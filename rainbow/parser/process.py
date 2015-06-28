import nltk
import string
from recurrent import RecurringEvent
import datetime

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
    'of': 'OF',
}

def process(sentence, one_time_event_chunker):
    sentence = sentence.replace('/', ' / ').lower()
    tokens = nltk.word_tokenize(sentence)
    default_tagger = nltk.data.load(nltk.tag._POS_TAGGER)
    tagger = nltk.tag.UnigramTagger(model=model, backoff=default_tagger)
    tagged = tagger.tag(tokens)
    result = one_time_event_chunker.parse(tagged)
    return result

def date_process(date):
    table = str.maketrans("", "", string.punctuation)
    date_string = ' '.join(date).translate(table)
    r = RecurringEvent(now_date=datetime.datetime(2010, 1, 1))
    onetimedate = r.parse(date_string)
    return onetimedate
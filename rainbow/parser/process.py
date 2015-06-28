import nltk
import string

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
}

def process(sentence, chunker):
    sentence = sentence.replace('/', ' / ')
    tokens = nltk.word_tokenize(sentence)
    default_tagger = nltk.data.load(nltk.tag._POS_TAGGER)
    tagger = nltk.tag.UnigramTagger(model=model, backoff=default_tagger)
    tagged = tagger.tag(tokens)
    result = chunker.parse(tagged)
    return result

def date_process(date):
    predicate = lambda x:x not in string.punctuation
    return filter(predicate, date)
__author__ = 'danielzuo'

import nltk
from rainbow.models.event import OneTimeEvent
import datetime

lemmatizer = nltk.WordNetLemmatizer()
stemmer = nltk.stem.porter.PorterStemmer()

sentence = "Graylock Event in San Mateo: June 21, 2015"

titlePattern = """
        NBAR:
            {<NN.*|JJ>*<NN.*>}

        NP:
            {<NBAR >}
    """

datePattern = """
            DATE:{<NNP><CD><,><CD>}
            """
DateChunker = nltk.RegexpParser(datePattern)
TitleChunker = nltk.RegexpParser(titlePattern)

def parse(text):
    events = [s.strip() for s in text.splitlines()]
    for event in events:
        formatted_sentence = format(event)
        noun_phrases = list(get_terms(formatted_sentence, "NP"))
        date = list(get_terms(formatted_sentence, "DATE"))
        date = list(date[0])
        noun_phrase = list(noun_phrases[0])
        formatted_date = datetime.datetime.strptime(' '.join(date),"%B %d %Y")
        formatted_title = ' '.join(noun_phrase)
        return OneTimeEvent(date=formatted_date, title=formatted_title).to_dict()

def format(sentence):
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)
    result = DateChunker.parse(tagged)
    result = TitleChunker.parse(result)
    return result

def leaves(tree, label):
    """Finds NP (nounphrase) leaf nodes of a chunk tree."""
    for subtree in tree.subtrees(filter = lambda t: t.label()==label):
        yield subtree.leaves()

def get_terms(tree, label):
    for leaf in leaves(tree, label):
        term = [ normalise(word) for word, tag in leaf
            if acceptable_word(word) ]
        yield term



def normalise(word):
    """Normalises words to lowercase and stems and lemmatizes it."""
    word = word.lower()
    word = stemmer.stem_word(word)
    word = lemmatizer.lemmatize(word)
    return word

def acceptable_word(word):
    """Checks conditions for acceptable word: length, stopword."""
    from nltk.corpus import stopwords
    stopwords = stopwords.words('english')

    accepted = bool(2 <= len(word) <= 40
        and word.lower() not in stopwords)
    return accepted

# nps = get_terms(result,"NP")
# print("NP:\n")
# for term in nps:
#         for word in term:
#            print(word)
#         print()
#
# dates = get_terms(result,"DATE")
# print("DATES:\n")
# for term in dates:
#         for word in term:
#            print(word)

parse(sentence)
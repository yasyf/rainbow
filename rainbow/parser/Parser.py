import nltk
from rainbow.models.event import OneTimeEvent
import datetime

class Parser():
    def __init__(self):
        self.oneTimeEventPattern = """
            DATE:{<NNP><CD><,><CD>}
            NBAR:
                {<NN.*|JJ>*<NN.*>}

            NP:
                {<NBAR >}
        """
        self.lemmatizer = nltk.WordNetLemmatizer()
        self.stemmer = nltk.stem.porter.PorterStemmer()

        self.testPattern = """
            TEST:{<CD><SLASH><CD>}
            """

        self.oneTimeEventChunker = nltk.RegexpParser(self.testPattern)

    def parse(self,text):
        events = [s.strip() for s in text.splitlines()]
        parsed_events = []
        for event in events:
            formatted_sentence = format(event)
            noun_phrases = list(self.get_terms(formatted_sentence, "NP"))
            date = list(self.get_terms(formatted_sentence, "DATE"))
            date = list(date[0])
            noun_phrase = list(noun_phrases[0])
            formatted_date = datetime.datetime.strptime(' '.join(date),"%B %d , %Y")
            formatted_title = ' '.join(noun_phrase)
            parsed_events.append(OneTimeEvent(date=formatted_date, title=formatted_title).to_dict())
        return parsed_events


    def format(self, sentence):
        tokens = nltk.word_tokenize(sentence)
        tagged = nltk.pos_tag(tokens)
        tagged = [(x, "SLASH") if x == '/' else (x, y) for (x, y) in tagged]
        result = self.oneTimeEventChunker.parse(tagged)
        #result.draw()
        return result


    def leaves(self, tree, label):
        """Finds NP (nounphrase) leaf nodes of a chunk tree."""
        for subtree in tree.subtrees(filter = lambda t: t.label()==label):
            yield subtree.leaves()


    def get_terms(self, tree, label):
        for leaf in self.leaves(tree, label):
            term = [ self.normalise(word) for word, tag in leaf
                if self.acceptable_word(word) ]
            yield term



    def normalise(self, word):
        """Normalises words to lowercase and stems and lemmatizes it."""
        #word = word.lower()
        #word = stemmer.stem_word(word)
        #word = lemmatizer.lemmatize(word)
        return word


    def acceptable_word(self, word):
        """Checks conditions for acceptable word: length, stopword."""
        return True
        #from nltk.corpus import stopwords
        #stopwords = stopwords.words('english')

        #accepted = bool(2 <= len(word) <= 40
        #    and word.lower() not in stopwords)
        #return accepted

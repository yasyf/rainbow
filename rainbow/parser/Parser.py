import nltk
from rainbow.models.event import OneTimeEvent
from rainbow.parser.process import *
import datetime

class Parser():
    def __init__(self):
        self.oneTimeEventPattern = """
            DATE:{<MONTH><CD><,>*<CD>|<CD><SLASH><CD>(<SLASH><CD>)* }
            NBAR:
                {<NN.*|JJ>*<NN.*>}

            NP:
                {<NBAR >}
        """

        self.oneTimeEventChunker = nltk.RegexpParser(self.oneTimeEventPattern)

    def parse(self,text):
        events = [s.strip() for s in text.splitlines()]
        parsed_events = []
        for event in events:
            formatted_sentence = process(event, self.oneTimeEventChunker)
            noun_phrases = next(self.get_terms(formatted_sentence, "NP"))
            date = next(self.get_terms(formatted_sentence, "DATE"))
            formatted_date = datetime.datetime.strptime(' '.join(date),"%B %d %Y")
            formatted_title = ' '.join(noun_phrases)
            parsed_events.append(OneTimeEvent(date=formatted_date, title=formatted_title).to_dict())
        return parsed_events


    def leaves(self, tree, label):
        """Finds NP (nounphrase) leaf nodes of a chunk tree."""
        for subtree in tree.subtrees(filter = lambda t: t.label()==label):
            yield subtree.leaves()


    def get_terms(self, tree, label):
        for leaf in self.leaves(tree, label):
            term = [ word for word, tag in leaf]
            yield term
import nltk
from rainbow.models.event import OneTimeEvent
from rainbow.parser.process import *
import datetime
from recurrent import RecurringEvent

class Parser():
    def __init__(self):
        self.date_pattern = """
            DATE:{<MONTH><CD><,>*<CD>|<CD><SLASH><CD>(<SLASH><CD>)*|<CD|JJ><OF><MONTH>}
        """
        self.title_pattern = """
            NP: {<PP\$>?<JJ.*>*<NN.*>+}
        """
        self.date_chunker = nltk.RegexpParser(self.date_pattern)
        self.title_chunker = nltk.RegexpParser(self.title_pattern)

    def parse(self,text):
        events = [s.strip() for s in text.strip().splitlines()]
        parsed_events = []
        for event in events:
            if event:
                try:
                    # attempt to match our title grammar
                    np_tagged = process(event, self.title_chunker)
                    noun_phrase = next(self.get_terms(np_tagged, "NP"))
                    formatted_title = ' '.join(noun_phrase)
                    try:
                        # attempt to match our date grammar
                        date_tagged = process(event, self.date_chunker)
                        date = next(self.get_terms(date_tagged, "DATE"))
                        ## format date as a datetime by calling dateprocess()
                        formatted_date = ""
                        parsed_events.append(OneTimeEvent(date=formatted_date, title=formatted_title))
                    except StopIteration:
                        #no date found, checking recurrent
                        
                        formatted_date = datetime.datetime.strptime(' '.join(date),"%B %d %Y")
                        formatted_title = ' '.join(noun_phrase)
                        parsed_events.append(OneTimeEvent(date=formatted_date, title=formatted_title).to_dict())
                except StopIteration:
                    # no title found, skip to next event
                    continue

        return parsed_events


    def leaves(self, tree, label):
        """Finds NP (nounphrase) leaf nodes of a chunk tree."""
        for subtree in tree.subtrees(filter = lambda t: t.label()==label):
            yield subtree.leaves()


    def get_terms(self, tree, label):
        for leaf in self.leaves(tree, label):
            term = [ word for word, tag in leaf]
            yield term

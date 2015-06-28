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
                    formatted_title = self.sanitize(' '.join(noun_phrase))
                    try:
                        # attempt to match our date grammar
                        date_tagged = process(event, self.date_chunker)
                        date = next(self.get_terms(date_tagged, "DATE"))
                        formatted_date = one_time_process(date)
                        parsed_events.append(OneTimeEvent(date=formatted_date, title=formatted_title))
                    except StopIteration:
                        #no date found, checking recurrent
                        if contains_date(event):
                            if is_recurring(event):
                                try:
                                    recurring_params = recurrent_parse(event)
                                    parsed_events.extend(recurrent_process(recurring_params, formatted_title))
                                except:
                                    print("exception")
                                    continue
                            else:
                                formatted_date = non_recurrent_parse(event)
                                parsed_events.extend(OneTimeEvent(date=formatted_date, title=formatted_title))
                        else:
                            # no date found, skip to next event
                            print('skip')
                            continue
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

    def sanitize(self, dirty_string):
        return dirty_string.strip()
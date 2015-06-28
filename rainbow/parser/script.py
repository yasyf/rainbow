from rainbow.parser.parser import Parser
from rainbow.parser.process import *

p = Parser()

trial = """
stuff every weekend

"""

events = p.parse(trial)

for event in events:
    print(event.to_dict())
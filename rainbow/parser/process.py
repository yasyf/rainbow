import nltk

def process(sentence, one_time_event_chunker):
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)
    tagged = [(x, "SLASH") if x == '/' else (x, y) for (x, y) in tagged]
    result = one_time_event_chunker.parse(tagged)
    #result.draw()
    print(result)
    return result

def date_preprocess(sentence):
    print()
import pandas as pd
import nltk
from nltk.corpus import stopwords
import collections
from app import source_names

def parser():
    '''
    Parses headlines
    '''
    headlines = pd.read_csv('headlines.csv')

    # operate on pandas dataframe to drop short headlines, empty entries, duplicates
    min_length = headlines['Title'].str.len() > 20
    not_null = headlines['Title'].notnull()
    headlines = headlines[not_null & min_length]
    headlines = headlines.drop_duplicates(subset=['Title'], keep='first')
        
    todays_headlines = {}

    for s in source_names:
        src = headlines['Source'] == s
        src = headlines[src]
        lines = {}
        stop = stopwords.words('english')


        for l in src['Title']:
            tokenized = nltk.word_tokenize(l)
            nouns = [word.lower() for word in tokenized if word.lower() not in stop]
            lines[l] = nouns

        count = {}

        for subj in lines.values():
            for w in subj:
                try:
                    count[w] += 1
                except KeyError:
                    count[w] = 1

        top_words = {}
        for w in range(0, 3):
            p = max(count, key=count.get)
            top_words[p] = []
            count[p] = 0

        ordered = collections.OrderedDict(sorted(top_words.items()))

        for h in src['Title']:
            for w in ordered.keys():
                if w.lower() in h.lower().split():
                    ordered[w].append(h)
        todays_headlines[s] = ordered
    return todays_headlines

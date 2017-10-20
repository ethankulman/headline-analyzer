from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from app import Word




def analyzer(today):
    sources = ['NyTimes', 'Breitbart', 'Huffington', 'Fox']
    to_plot = {}
    for s in sources:
        news = today[s]
        src = []
        for w in news:
            stories = news[w]
            headlines = []
            sentiment = 0
            magnitude = 0
            avg_sent = 0
            avg_mag = 0
            for h in stories:
                client = language.LanguageServiceClient()
                document = types.Document(content=unicode(h),
                          type=enums.Document.Type.PLAIN_TEXT)
                sent = client.analyze_sentiment(document=document).document_sentiment
                if sent.score != 0:
                    sentiment += sent.score
                    magnitude += sent.magnitude
                    headlines.append(h)
            total = len(headlines)
            if total > 0:
                avg_sent = sentiment/total
                avg_mag = magnitude/total
                word = Word(word=w, source=s, headlines=headlines, sentiment=avg_sent, magnitude=avg_mag)
            src.append([w, avg_sent, avg_mag])
        to_plot[s] = src
    return to_plot



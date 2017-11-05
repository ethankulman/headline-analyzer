from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import app




def analyzer(today):
    agencies = ['NyTimes', 'Breitbart', 'Huffington', 'Fox']
    to_plot = {}
    for s in agencies:
        news = today[s]
        src = []
        for w in news:
            stories = news[w]
            total_headlines = 0
            sentiment = 0
            magnitude = 0
            avg_sent = 0
            avg_mag = 0
            for h in stories:
                client = language.LanguageServiceClient()
                document = types.Document(content=str(h),
                          type=enums.Document.Type.PLAIN_TEXT)
                sent = client.analyze_sentiment(document=document).document_sentiment
                if sent.score != 0:
                    total_headlines += 1
                    if total_headlines == 1:
                        word = app.Word(word=w, source=s)
                        app.db.session.add(word)
                        app.db.session.flush()
                    sentiment += sent.score
                    magnitude += sent.magnitude
                    print(word.id)
                    print(word)
                    headline = app.Headline(h, word.id)
                    app.db.session.add(headline)

            if total_headlines:
                avg_sent = sentiment/total_headlines
                avg_mag = magnitude/total_headlines
                word.sentiment = avg_sent
                word.magnitude = avg_mag
                app.db.session.add(word)
            app.db.session.commit()
            src.append([w, avg_sent, avg_mag])
        to_plot[s] = src
    return to_plot



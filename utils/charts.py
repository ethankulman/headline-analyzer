import app
import plotly.plotly as py
import plotly.graph_objs as go
from plotly import tools
import plotly
import pandas as pd
plotly.tools.set_credentials_file(username='ethankulman', api_key='X3AcpgRUt9w6cM2vhmLv')


def daily_split(to_plot):
    sources = ['NyTimes', 'Breitbart', 'Huffington', 'Fox']
    fig = tools.make_subplots(rows=1, cols=4, specs=[[{}, {}, {}, {}]],
                              shared_xaxes=True, shared_yaxes=True)
    for s in range(0, 4):
        src = sources[s]
        words = to_plot[src]
        agency = go.Scatter(
            x=[src, src, src],
            y=[words[0][1], words[1][1], words[2][1]],
            mode='markers+text',
            textposition='bottom',
            name=src,
            text=[words[0][0].capitalize(), words[1][0].capitalize(), words[2][0].capitalize()],
        )
        fig.append_trace(agency, 1, s+1)

    fig['layout'].update(height=600, width=800, title="Top Words From Today's Headlines",
                         xaxis=dict(title='News Agency'), yaxis=dict(title='Sentiment'))
    py.plot(fig, filename='daily-words', auto_open=False)


'''
def trump_tracker():
    nytimes = app.Word.query.filter_by(word="trump", source="NyTimes").all()
    breit = app.Word.query.filter_by(word="trump", source="Breitbart").all()
    fox = app.Word.query.filter_by(word="trump", source="Fox").all()
    huff = app.Word.query.filter_by(word="trump", source="Huffington").all()
    trump_sources = [nytimes, breit, fox, huff]
    srcs = {}
    for s in trump_sources:
        dates = []
        sentiment = []
        magnitude = []
        for d in s:
            dates.append(d.date)
            sentiment.append(d.sentiment)
            magnitude.append(d.magnitude)

        srcs[s[0].source] = [dates, sentiment, magnitude]
    print(srcs)

    print("nyt: ", nytimes.source)
    print("breit: ", breit.source)
    print("fox: ", fox.source)
    print("huff: ", huff.source)
    fig = tools.make_subplots(rows=1, cols=4, specs=[[{}, {}, {}, {}]],
                             shared_xaxes=True, shared_yaxes=True)

    for s in range(0, 4):
        agency = go.Scatter(
            x=[src, src, src],
            y=[words[0][1], words[1][1], words[2][1]],
            mode='lines+text',
            textposition='bottom',
            name=src,
            text=[words[0][0].capitalize(), words[1][0].capitalize(), words[2][0].capitalize()],
        )
        fig.append_trace(agency, 1, s+1)

    fig['layout'].update(height=600, width=800, title="Sentiment Towards Trump",
                         xaxis=dict(title='Date'), yaxis=dict(title='Sentiment'))
    py.plot(fig, filename='daily-words', auto_open=True)

'''
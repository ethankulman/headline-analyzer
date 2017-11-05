import app
import plotly.plotly as py
import plotly.graph_objs as go
from plotly import tools
import plotly
import pandas as pd
plotly.tools.set_credentials_file(username='ethankulman', api_key='X3AcpgRUt9w6cM2vhmLv')


def daily_split(to_plot):
    sources = ['NyTimes', 'Breitbart', 'Huffington', 'Fox']
    fig = tools.make_subplots(rows=1, cols=1, specs=[[{}]],
                              shared_xaxes=True, shared_yaxes=True, horizontal_spacing=0.001)
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
        fig.append_trace(agency, 1, 1)

    fig['layout'].update(height=600, width=800, title="Top Words From Today's Headlines",
                         xaxis=dict(title='News Agency'), yaxis=dict(title='Sentiment'))
    py.plot(fig, filename='daily-words', auto_open=False)



def trump_tracker():
    sources = ['NyTimes', 'Breitbart', 'Huffington', 'Fox']

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
            dates.append(d.date.strftime("%Y-%m-%d"))
            sentiment.append(d.sentiment)
            magnitude.append(d.magnitude)

        srcs[s[0].source] = [dates, sentiment, magnitude]
    print(srcs)

    print("nyt: ", nytimes[0].source, breit[0].word)
    print("breit: ", breit[0].source, breit[0].word)
    print("fox: ", fox[0].source, fox[0].word)
    print("huff: ", huff[0].source, huff[0].word)
    data = []

    for s in range(0, 4):
        agency = go.Scatter(
            x=srcs[sources[s]][0],
            y=srcs[sources[s]][1],
            mode='lines+markers',
            name=sources[s],
        )
        data.append(agency)

    layout = dict(height=600, width=800, title="Sentiment Towards Trump",
                         xaxis=dict(title='Date'), yaxis=dict(title='Sentiment'))
    fig = dict(data=data, layout=layout)
    py.plot(fig, filename='trump_tracker', auto_open=True)

import app
import plotly.plotly as py
import plotly.graph_objs as go
from app.
from plotly import tools
import plotly
import pandas as pd
# set plotly credentials

def plot_top_words(to_plot, num_top_words=3):
    '''
    Plots the most common headline phrases from each news source
    '''
    fig = tools.make_subplots(rows=1, cols=1, specs=[[{}]],
                              shared_xaxes=True, shared_yaxes=True, horizontal_spacing=0.001)

    # go through each source
    for name in range(len(source_names)):

        src = source_names[name]

        words = to_plot[src]

        # plot the top 3 most common words
        agency = go.Scatter(
            x=[src]*num_top_words,
            y=[words[i][1] for i in range(0,num_top_words)],
            mode='markers+text',
            textposition='bottom',
            name=src,
            text=[words[i][0].capitalize() for i in range(0,num_top_words)],
        )

        fig.append_trace(agency, 1, 1)

    fig['layout'].update(height=600, width=800, title="Top Words From Today's Headlines",
                         xaxis=dict(title='News Agency'), yaxis=dict(title='Sentiment'))
    py.plot(fig, filename='daily-words', auto_open=False)



def trump_tracker():

    trump_sources = [app.Word.query.filter_by(word="trump", source=src).all() for src in source_names]

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

    data = []

    for s in range(0, len(source_names)):
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

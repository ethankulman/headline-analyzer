import plotly.plotly as py
import plotly.graph_objs as go
from plotly import tools
import plotly
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

    fig['layout'].update(height=600, width=600, title="Top Words From Today's Headlines")
    py.plot(fig, filename='daily-words')
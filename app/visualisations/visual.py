import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def draw_piechart(df):

    fig = px.pie(df,
                 values=df[['error_shortage', 'error_excess']].abs().values.tolist()[0],
                 names=['error_shortage', 'error_excess'],
                 hole=.3)
    return fig


def draw_error_plot(df):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['forecast'],
            name='forecast'
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['yeild'],
            name='yeild'
        )
    )
    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df['error_shortage'],
            name='error_shortage'

        )
    )
    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df['error_excess'],
            name='error_excess'
        )
    )
    return fig


def draw_all_station_chart(df, sort_by='yeild'):
    df = df.sort_values(sort_by, ascending=False)
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df.index.get_level_values(0),
            y=df.yeild,
            name='yeild'

        )
    )
    fig.add_trace(
        go.Scatter(
            x=df.index.get_level_values(0),
            y=df.forecast,
            name='forecast'
        )
    )
    fig.add_trace(
        go.Bar(
            x=df.index.get_level_values(0),
            y=df.error_shortage,
            name='error_shortage'
        )
    )
    fig.add_trace(
        go.Bar(
            x=df.index.get_level_values(0),
            y=df.error_excess,
            name='error_excess'
        )
    )
    return fig


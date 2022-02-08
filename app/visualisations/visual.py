import plotly.express as px
import pandas as pd


def draw_piechart(df):

    fig = px.pie(df,
                 values=df[['error_shortage', 'error_excess']].abs().values.tolist()[0],
                 names=['error_shortage', 'error_excess'],
                 hole=.3)
    return fig

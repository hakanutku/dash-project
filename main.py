import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import sqlite3

conn = sqlite3.connect("twitter.db")
c = conn.cursor()


def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS Twitter")


app = dash.Dash(__name__)

colors = {
    'background': '#111333',
    'text': '#7FDBFF'
}

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_usa_states.csv')


app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    dcc.Graph(
        id='example_graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [3, 6, 9], 'type': 'bar', 'name': 'example'}
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                },
                'title': 'Dash Data Visualization'
            }
        }
    ),
    dcc.Graph(
        id='example_graph2',
        figure={
            'data': [go.Table(
                header=dict(values=list(df.columns),
                            line=dict(color='#7D7F80'),
                            fill=dict(color='#a1c3d1')),
                cells=dict(values=[df[column] for column in df.columns]),
            )],
            'layout': {
                'title': 'Example - 2'
            }
        }
    )
])
# @app.callback(Output(),)
# def update_graph():
#     data = pd.read_sql("SELECT * FROM Twitter", conn)


if __name__ == '__main__':
    app.run_server()

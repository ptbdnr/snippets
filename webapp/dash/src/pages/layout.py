import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

dash.register_page(__name__)


# Sample data for the bar chart
data = {"data": [1, 5, 2, 6, 2, 1]}
df = pd.DataFrame(data)

layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Tab1', children=[
            html.H2("Tab1"),
            html.P("Some text")
        ]),
        dcc.Tab(label='Tab2', children=[
            html.H2("Tab2"),
            html.P("Some text")
        ])
    ]),
    html.Hr(),
    html.Div([
        html.Div([
            html.H2("Column1"),
            html.P("Some text")
        ], style={'width': '48%', 'display': 'inline-block'}),
        html.Div([
            html.H2("Column2"),
            html.P("Some text")
        ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
    ]),
    html.Hr(),
    dcc.Graph(
        id='bar-chart',
        figure=px.bar(df, y='data')
    ),
    html.Details([
        html.Summary("Expander"),
        html.P("Some text"),
        html.Code("... and more")
    ]),
    html.Hr(),
    html.Div([
        html.Label("What's your name?"),
        dcc.Input(id='name-input', type='text', value=''),
        html.Br(),
        dcc.Checklist(
            options=[{'label': 'Show item.', 'value': 'yes'}],
            value=['yes'],
            id='toggle-checkbox'
        ),
        html.Div(id='name-output'),
        html.Div(id='toggle-output')
    ]),
    html.Hr(),
    html.Footer("some footnote")
])


@callback(
    Output('name-output', 'children'),
    Output('toggle-output', 'children'),
    Input('name-input', 'value'),
    Input('toggle-checkbox', 'value')
)
def update_output(name, toggled):
    name_output = f"Your name: {name}"
    toggled_output = "This is toggled." if 'yes' in toggled else ""
    return name_output, toggled_output


if __name__ == "__main__":
    myapp = Dash(__name__)
    myapp.layout = layout
    myapp.run_server(debug=True)

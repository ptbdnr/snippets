import dash
from dash import html

dash.register_page(__name__, path='/')

layout = html.Div([
    html.H1('Title'),
    html.Div('v0.0.1'),
])


if __name__ == "__main__":
    myapp = dash.Dash(__name__)
    myapp.layout = layout
    myapp.run_server(debug=True)

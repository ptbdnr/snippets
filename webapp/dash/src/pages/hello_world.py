import dash
from dash import Dash, html, dcc, callback, Output, Input, State


dash.register_page(__name__)


toaster_visible_style = {'display': 'block', 'position': 'fixed', 'top': '10px', 'right': '10px', 'backgroundColor': 'lightgrey', 'padding': '10px', 'border': '1px solid black'}
toaster_hidden_style = {'display': 'none'}


layout = html.Div([
    html.H1("Hello, World!"),
    html.Button("Click me", id="click-me-button", n_clicks=0),
    html.Div(id="new-text"),
    dcc.Interval(id='interval', interval=3000, n_intervals=0, disabled=True),
    html.Div("You clicked the button!", id='toaster', style=toaster_visible_style)
])


@callback(
    Output("new-text", "children"),
    Output("toaster", "style"),
    Output("interval", "disabled"),
    Input("click-me-button", "n_clicks"),
    Input("interval", "n_intervals"),
    State("toaster", "style")
)
def display_link(n_clicks, n_intervals, toaster_style):
    ctx = dash.callback_context

    if not ctx.triggered:
        return "", {'display': 'none'}, True

    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    output_div = html.Div([
        html.A("wikipedia.org", href="https://wikipedia.org", target="_blank")
    ])

    if trigger_id == "click-me-button":
        return output_div, toaster_visible_style, False
    elif trigger_id == "interval":
        return output_div, toaster_hidden_style, True

    return "", toaster_style,  True


if __name__ == "__main__":
    myapp = Dash(__name__)
    myapp.layout = layout
    myapp.run_server(debug=True)

import dash
from dash import Dash, html, dcc, callback, Output, Input, State

dash.register_page(__name__)


def get_items():
    return [{'id': 1, 'title': 'item 1'}, {'id': 2, 'title': 'item 2'}]


layout = html.Div([

    html.Div(id='form3-output'),

    # Form 1
    html.Div([
        html.H2("Form 1"),
        dcc.Dropdown(
            id='framework-dropdown',
            options=[
                {'label': 'A', 'value': 'A'},
                {'label': 'B', 'value': 'B'}
            ],
            value='A'
        ),
        dcc.Textarea(
            id='text-area',
            style={'width': '100%', 'height': 80},
            value=''
        ),
        html.Button('Submit', id='submit-button', n_clicks=0),
        html.Div(id='form1-output')
    ]),

    # Form 2
    html.Div([
        html.H2("Form 2"),
        html.Div([
            html.Button('button A', id='button-a', n_clicks=0),
            html.Button('button B', id='button-b', n_clicks=0)
        ], style={'display': 'flex', 'justify-content': 'space-between'}),
        html.Div(id='form2-output')
    ]),

    # Form 3
    html.Button('button D', id='button-d', n_clicks=0)
])


@callback(
    Output('form1-output', 'children'),
    Input('submit-button', 'n_clicks'),
    State('text-area', 'value')
)
def handle_form1_submit(n_clicks, text_value):
    if n_clicks > 0:
        return html.Div([
            html.P('output'),
            html.P(f'input: {text_value}')
        ])
    return ''


@callback(
    Output('form2-output', 'children'),
    Input('button-a', 'n_clicks'),
    Input('button-b', 'n_clicks')
)
def handle_form2_buttons(n_clicks_a, n_clicks_b):
    ctx = dash.callback_context
    if not ctx.triggered:
        return ''

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if button_id == 'button-a' and n_clicks_a > 0:
        items = get_items()
        return html.Div([
            html.H3('A list'),
            html.P('A list'),
            html.Table([
                html.Tr([html.Th('ID'), html.Th('Title')])] +
                [html.Tr([html.Td(item['id']), html.Td(item['title'])]) for item in items]
            )
        ])
    elif button_id == 'button-b' and n_clicks_b > 0:
        items = get_items()
        return html.Div([
            html.H3('B list'),
            html.P('B list'),
            html.Table([
                html.Tr([html.Th('ID'), html.Th('Title')])] +
                [html.Tr([html.Td(item['id']), html.Td(item['title'])]) for item in items]
            )
        ])
    return ''


@callback(
    Output('form3-output', 'children'),
    Input('button-d', 'n_clicks'),
)
def handle_form3_buttons(n_clicks):
    ctx = dash.callback_context
    if not ctx.triggered:
        return ''

    if n_clicks > 0:
        items = get_items()
        return html.Div([
            html.H3('D list'),
            html.P('D list'),
            html.Table([
                html.Tr([html.Th('ID'), html.Th('Title')])] +
                [html.Tr([html.Td(item['id']), html.Td(item['title'])]) for item in items]
            )
        ])
    return ''


if __name__ == "__main__":
    myapp = Dash(__name__)
    myapp.layout = layout
    myapp.run_server(debug=True)

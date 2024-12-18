import dash
from dash import Dash, html, dcc, callback, Output, Input, State

dash.register_page(__name__)


_LOREM_IPSUM = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam eu est quis turpis mattis aliquam a non justo. Sed libero nibh, lacinia dignissim tincidunt vel, congue vel erat. Pellentesque porta augue ac diam convallis, malesuada lacinia mi ultricies. Maecenas sodales odio vel lacinia pellentesque. Vivamus erat sapien, feugiat vitae orci euismod, accumsan imperdiet est. Nulla tempor erat mattis, mollis quam a, pellentesque magna. Cras lectus est, luctus non nisl nec, eleifend dictum risus. Aenean vestibulum posuere est, a ultricies ex consectetur nec. Nullam quis tempus diam. Quisque semper et sapien ac mollis. Nullam viverra risus a scelerisque imperdiet.

Vivamus eleifend scelerisque augue vitae egestas. Phasellus auctor nisi in lacus volutpat, id commodo leo auctor. Donec sit amet nisl nec leo pretium sollicitudin et sit amet risus. Sed in nisl eget nibh pretium vehicula in vel felis. Nunc ut scelerisque tortor, eu gravida diam. In hac habitasse platea dictumst. Nulla facilisi. Nam at augue nec velit laoreet rhoncus. Proin consectetur semper vulputate.
"""


layout = html.Div([
    dcc.Input(id='chat-input', type='text', placeholder='Say something'),
    html.Button('Send', id='send-button', n_clicks=0),
    html.Div(id='chat-output'),
])

messages = []


@callback(
    Output('chat-output', 'children'),
    Input('send-button', 'n_clicks'),
    State('chat-input', 'value')
)
def update_chat(n_clicks, value):
    ctx = dash.callback_context

    if not ctx.triggered:
        return render_messages(), True

    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'send-button' and n_clicks > 0 and value:
        messages.append({'role': 'user', 'content': value})
        messages.append({'role': 'assistant', 'content': _LOREM_IPSUM})
        return render_messages(), False

    return render_messages(), True


def render_messages():
    return html.Div([
        html.Div([
            html.Span('🦄' if msg['role'] == 'user' else '🤖'),
            html.Span(msg['role'], style={'fontWeight': 'bold'}),
            html.Span(msg['content'])
        ]) for msg in messages
    ])


if __name__ == "__main__":
    myapp = Dash(__name__)
    myapp.layout = layout
    myapp.run_server(debug=True)

import os

import dotenv

import dash
from dash import Dash, html, dcc
import dash_auth

dotenv.load_dotenv()
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

app = Dash(__name__, use_pages=True)

# Add basic auth
dash_auth.BasicAuth(app, username_password_list={USERNAME: PASSWORD})

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.Div([
            html.Img(src="/media/Smiley.svg.png", style={'width': '30px'}),
            html.Ul([
                html.Li(
                    dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
                ) for page in dash.page_registry.values()
            ], style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '10px', 'backgroundColor': '#f0f0f0'}),
            html.Div([
                dash.page_container
            ], style={'width': '75%', 'display': 'inline-block', 'padding': '10px'})
        ], style={'display': 'flex'})
    ]
)

if __name__ == "__main__":
    app.run(debug=True)

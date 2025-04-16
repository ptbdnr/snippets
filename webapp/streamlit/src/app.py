import os
import logging

import streamlit as st
from dotenv import load_dotenv
from streamlit_theme import st_theme

from password import check_password
from src.components.hello import component as hello_component
from src.components.forms import component as forms_component
from src.components.chat import component as chat_component
from src.components.layout import component as layout_component
from src.components.crud import component as crud_component


# Load environment variables
load_dotenv(".env")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.formatter = logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger.addHandler(handler)

def initialize_session_state() -> None:
    """Initialize the session state variables if they are not already set."""
    env_vars = {
        "FOO": "FOO",
        "BAR": "BAR",
        "BAR": "BAR",
    }
    for var, env in env_vars.items():
        if var not in st.session_state:
            value = os.getenv(env)
            if value is None:
                message = "Missing env variable: " + env
                logger.exception(message)
                # raise ValueError(message)
            st.session_state[var] = value

# Initialize the session state variables
initialize_session_state()

# Set the page layout to wide
st.set_page_config(
    page_title="Snippets",
    page_icon="static/kainos_icon.png", # or "🔥"
    layout="wide",
)

# if not check_password():
#     st.stop()  # Do not continue if check_password is not True.

theme = st_theme()
if theme and theme.get("base") == "dark":
    st.logo(
        image='media/Smiley.svg.png',
        size='medium',
        link='https://en.wikipedia.org/wiki/Smiley',
    )

component_map = {
    "Hello": {"icon": "📙", "component": hello_component, "url_path": "hello"},
    "Forms": {"icon": "📝", "component": forms_component, "url_path": "forms"},
    "Chat": {"icon": "💬", "component": chat_component, "url_path": "chat"},
    "Layout": {"icon": "📊", "component": layout_component, "url_path": "layout"},
    "CRUD": {"icon": "🗂️", "component": crud_component, "url_path": "crud"},
}
DEFAULT_PAGE_TITLE = "Hello"

# Main Streamlit app starts here

# Header
with st.container():
    col1, col2 = st.columns([250, 800])
    col1.image(
        image="media/Smiley.svg.png",
        caption="Smiley",
        use_container_width=True,
    )
    col2.title("Title")
    col2.subheader('v0.0.1')

# Side panel navigation
pages = [st.Page(page=c["component"], title=k, icon=c["icon"], url_path=c["url_path"], default=(k==DEFAULT_PAGE_TITLE)) 
         for k, c in component_map.items()]
pg = st.navigation(
    pages=pages,
    position="sidebar",
    expanded=True,
)

# Custom CSS
css = """
<style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size:1.5rem;
    }
</style>
"""

st.markdown(css, unsafe_allow_html=True)

pg.run()

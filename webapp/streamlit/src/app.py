import os
import logging

import streamlit as st
from dotenv import load_dotenv
from streamlit_theme import st_theme

from password import check_password

# Load environment variables
load_dotenv(".env.local")

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

if not check_password():
    st.stop()  # Do not continue if check_password is not True.

theme = st_theme()
if theme and theme.get("base") == "dark":
    st.logo(
        image='media/Smiley.svg.png',
        size='medium',
        link='https://en.wikipedia.org/wiki/Smiley',
    )

# Main Streamlit app starts here

# Header
with st.container():
    col1, col2 = st.columns([250, 800])
    col1.image(
        image="media/Smiley.svg.png",
        caption="Smiley",
        use_column_width=True,
    )
    col2.title("Title")
    col2.subheader('v0.0.1')

# Side panel navigation
pg = st.navigation(
    pages=[
        st.Page("pages/hello_world.py", title="HelloWord", icon=":material/thumb_up:", default=True),
        st.Page("pages/forms.py", title="Forms", icon="📝"),
        st.Page("pages/chat.py", title="Chat", icon="💬"),
        st.Page("pages/layout.py", title="Layout", icon="📊"),
    ],
    # position="sidebar",
    # expanded=True,
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

import logging

import streamlit as st

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)

ITEM_CATEGORY = "World"

def component() -> None:
    """Render component."""
    st.header(f"Hello {ITEM_CATEGORY.title()}")

    button = st.button("Click me")
    if button:
        st.toast('You clicked the button!', icon="🔥")
        st.markdown("[wikipedia](www.wikipedia.com)")

    with st.sidebar:
        st.write("This is a sidebar in the Hello World page.")

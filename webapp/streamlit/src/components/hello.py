import streamlit as st

import src.components.template as template

def component() -> None:
    """Render component for the tab."""

    template.ITEM_CATEGORY = "World"
    template.component()

    
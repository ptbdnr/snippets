from __future__ import annotations

import logging
from typing import Optional

import extra_streamlit_components as stx
import requests
import streamlit as st

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)

STATUS_CODE_OK = 200
DEFAULT_TIMEOUT = 300
ITEM_GROUP_NAME = "foo"

def get_item(
    item_id: Optional[str] = None,
) -> list[dict]:
    """Query the data."""
    url = f"{st.session_state['BACK_API_BASE_URL']}/{ITEM_GROUP_NAME}s/"
    if item_id:
        url += item_id
    logger.debug("GET %s", url)
    response = requests.get(url=url, timeout=DEFAULT_TIMEOUT)
    logger.debug("Response: %s", response.text)
    if response.status_code == STATUS_CODE_OK:
        logger.debug("Request completed successfully to %s", url)
        return response.json()
    msg = f"Failed to complete request. Status code: {response.status_code}"
    raise ValueError(msg)

def put_item(
    item_id: str,
    data: dict,
) -> dict:
    """Post a payload."""
    url = f"{st.session_state['BACK_API_BASE_URL']}/{ITEM_GROUP_NAME}s/{item_id}"
    logger.debug("PUT %s", url)
    logger.debug("Data: %s", data)
    response = requests.put(
        url=url,
        headers={"Content-Type": "application/json"},
        data=data,
        timeout=DEFAULT_TIMEOUT,
    )
    logger.debug("Response: %s", response.text)
    if response.status_code == STATUS_CODE_OK:
        logger.debug("Request posted successfully to %s", url)
        return response.json()
    msg = f"Failed to post request. Status code: {response.status_code}"
    raise ValueError(msg)

def delete_item(
    item_id: str,
) -> dict:
    """Delete an item."""
    url = f"{st.session_state['BACK_API_BASE_URL']}/{ITEM_GROUP_NAME}s/{item_id}"
    logger.debug("DELETE %s", url)
    response = requests.delete(url=url, timeout=DEFAULT_TIMEOUT)
    logger.debug("Response: %s", response.text)
    if response.status_code == STATUS_CODE_OK:
        logger.debug("Request completed successfully to %s", url)
        return response.json()
    msg = f"Failed to complete request. Status code: {response.status_code}"
    raise ValueError(msg)

def component() -> None:
    """Render component."""
    st.header(f"{ITEM_GROUP_NAME.title()}s")

    viewer()
    st.divider()
    updater()
    st.divider()
    deleter()

def viewer() -> None:
    """Render component for the viewer."""
    with st.container():

        st.header(f"👁️ View {ITEM_GROUP_NAME}s")

        chosen_id = stx.tab_bar(data=[
            stx.TabBarItemData(id="All", title="📜 All", description=f"View all {ITEM_GROUP_NAME}s"),
            stx.TabBarItemData(id="One", title="📌 One", description=f"View one {ITEM_GROUP_NAME}"),
        ])

        placeholder = st.container()
        if chosen_id == "All":
            viewer_item_id = None
        elif chosen_id == "One":
            viewer_item_id = placeholder.text_input(key="viewer_item_id", label=f"{ITEM_GROUP_NAME.title()} ID" )

        button = placeholder.button("View")

        if button:
            try:
                st.toast("Start query", icon="⏳")
                with st.spinner("Processing..."):
                    viewer_item_id = str(viewer_item_id) if chosen_id == "One" else None
                    response = get_item(
                        item_id=viewer_item_id,
                    )
                if response:
                    st.toast("Processing done", icon="✅")
                    st.success("Processing completed successfully.")
                    with st.expander(f"See {ITEM_GROUP_NAME}s", expanded=True):
                        st.table(response)
            except Exception as ex:
                st.toast(
                    body="An error occurred while processing the request.",
                    icon="⚠️",
                )
                logging.exception(msg=ex)
                st.exception(ex)

def updater() -> None:
    """Render component."""
    with st.container():

        st.header(f"✏️ Update {ITEM_GROUP_NAME}")

        updater_item_id = st.text_input(
            key=f"updater_{ITEM_GROUP_NAME}_id",
            label=f"{ITEM_GROUP_NAME.title()} ID",
            value="A1",
        )

        item_content = st.text_area(label="Content")

        button = st.button("Update")

        if button:
            try:
                st.toast("Start query", icon="⏳")
                with st.spinner("Processing..."):
                    body = {
                        "content": item_content,
                    }
                    response = put_item(
                        item_id=str(updater_item_id),
                        data=body,
                    )
                if response:
                    st.toast("Processing done", icon="✅")
                    st.success("Processing completed successfully.")
                    with st.expander("See response", expanded=False):
                        st.table(response)
            except Exception as ex:
                st.toast(
                    body="An error occurred while processing the request.",
                    icon="⚠️",
                )
                logging.exception(msg=ex)
                st.exception(ex)

def deleter(
    item_id: Optional[str] = None,
) -> None:
    """Render component."""
    with st.container():

        st.header(f"🗑️ Delete {ITEM_GROUP_NAME}")

        item_id = st.text_input(
            key=f"deleter_{ITEM_GROUP_NAME}_id",
            label=f"{ITEM_GROUP_NAME.title()} ID",
            value="A1",
        )

        button = st.button("Delete")

        if button:
            try:
                st.toast("Start query", icon="⏳")
                with st.spinner("Processing..."):
                    response = delete_item(
                        item_id=str(item_id),
                    )
                if response:
                    st.toast("Processing done", icon="✅")
                    st.success("Processing completed successfully.")
                    with st.expander("See response", expanded=False):
                        st.table(response)
            except Exception as ex:
                st.toast(
                    body="An error occurred while processing the request.",
                    icon="⚠️",
                )
                logging.exception(msg=ex)
                st.exception(ex
)
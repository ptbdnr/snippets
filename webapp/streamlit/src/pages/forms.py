import logging
import time
from typing import List, Dict

import streamlit as st


def get_items() -> List[Dict]:
    time.sleep(2)
    return [{'id': 1, 'title': 'item 1'}, {'id': 2, 'title': 'item 2'}]


with st.form(key='rows') as f_input:

    framework_key = st.selectbox(
        label='select one',
        options=['A', 'B']
    )

    text_input = st.text_area(
        label='text area',
        height=80)

    button = st.form_submit_button('Submit')

    if button:
        try:
            st.toast('start processing')
            st.text('output')
            st.write('input: ' + text_input)
        except Exception as ex:
            st.toast(
                body="An error occurred while processing the request.",
                icon="⚠️",
            )
            logging.exception(msg=ex)
            st.exception(ex) 


with st.form(key='columns') as f_database:

    col1, col2 = st.columns([1, 1])

    with col1:
        button_a = st.form_submit_button('button A')
    with col2:
        button_b = st.form_submit_button('button B')

    if button_a:
        try:
            st.toast('pressed button a')
            st.toast("start processing", icon="⏳")
            start_time = time.time()
            with st.spinner('querying only...'):
                item_list = get_items()
            end_time = time.time()
            st.toast(
                body=f"completed in {end_time - start_time:.2f} seconds",
                icon="🎉",
            )
            st.subheader('A list')
            st.write('A list')
            st.table(item_list)
        except Exception as ex:
            st.toast(
                body="An error occurred while processing the request.",
                icon="⚠️",
            )
            logging.exception(msg=ex)
            st.exception(ex)

    if button_b:
        try:
            st.toast('pressed button B')
            with st.spinner('querying only...'):
                item_list = get_items()
                st.subheader('B list')
                st.write('B list')
                st.table(item_list)
        except Exception as ex:
            st.toast(
                body="An error occurred while processing the request.",
                icon="⚠️",
            )
            logging.exception(msg=ex)
            st.exception(ex)

with st.form(key='callback') as f_callback:

    def clickHandler(buttonName: str):
        try:
            st.toast(f'pressed button {buttonName}')
            with st.spinner('querying only...'):
                item_list = get_items()
                st.subheader(f'{buttonName} list')
                st.write(f'{buttonName} list')
                st.table(item_list)
        except Exception as ex:
            st.toast(
                body="An error occurred while processing the request.",
                icon="⚠️",
            )
            logging.exception(msg=ex)
            st.exception(ex)

    button_d = st.form_submit_button('button D', on_click=clickHandler, args=('D'))

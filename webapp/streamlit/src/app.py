import os
import logging
import requests
from typing import List, Dict

import dotenv

import streamlit as st

from src.password import check_password


if not check_password():
    st.stop()  # Do not continue if check_password is not True.


dotenv.load_dotenv()


def get_items() -> List[Dict]:
    return [{'id': 1, 'title': 'item 1'}, {'id': 2, 'title': 'item 2'}]


# Main Streamlit app starts here
st.title('Title')
st.text('v0.0.1')


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
        except Exception as ex:
            logging.exception(ex)
            st.exception(ex) 


with st.form(key='columns') as f_database:
    
    col1, col2 = st.columns([1,1])

    with col1:
        button_a = st.form_submit_button('button A')
    with col2:
        button_b = st.form_submit_button('button B')
    
    if button_a:
        try:
            st.toast('pressed button a')
            item_list = get_items()
            st.write('A list')
            st.table(item_list)
        except Exception as ex:
            logging.exception(ex)
            st.exception(ex) 
    
    if button_b:
        try:
            st.toast('pressed button b')
            item_list = get_items()
            st.write('B list')
            st.table(item_list)
        except Exception as ex:
            logging.exception(ex)
            st.exception(ex)

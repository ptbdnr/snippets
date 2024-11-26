import os
import logging
import requests
import time
from typing import List, Dict

import streamlit as st

import dotenv

dotenv.load_dotenv()


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
            with st.spinner('querying only...'):
                item_list = get_items()
            st.subheader('A list')
            st.write('A list')
            st.table(item_list)
        except Exception as ex:
            logging.exception(ex)
            st.exception(ex) 
    
    if button_b:
        try:
            st.toast('pressed button b')
            with st.spinner('querying only...'):
                item_list = get_items()
                st.subheader('B list')
                st.write('B list')
                st.table(item_list)
        except Exception as ex:
            logging.exception(ex)
            st.exception(ex)

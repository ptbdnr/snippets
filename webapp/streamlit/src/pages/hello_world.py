import streamlit as st

st.header("Hello World")

with st.sidebar:
    st.write("This is a sidebar in the Hello World page.")
    st.markdown("[wikipedia](www.wikipedia.com)")
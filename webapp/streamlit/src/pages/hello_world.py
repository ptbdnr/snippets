import streamlit as st

st.header("Hello World")

button = st.button("Click me")
if button:
    st.toast('You clicked the button!', icon="🔥")
    st.markdown("[wikipedia](www.wikipedia.com)")

with st.sidebar:
    st.write("This is a sidebar in the Hello World page.")

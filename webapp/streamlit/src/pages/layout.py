import streamlit as st

with st.container():
    tab1, tab2 = st.tabs(["Tab1", "Tab2"])

    with tab1:
        st.header("Tab1")
        st.write("Some text")

    with tab2:
        st.header("Tab2")
        st.write("Some text")

st.divider()

with st.container():
    col1, col2 = st.columns([1,1])

    with col1:
        st.header("Column1")
        st.write("Some text")
    with col2:
        st.header("Column2")
        st.write("Some text")


st.divider()

with st.container():
    st.bar_chart({"data": [1, 5, 2, 6, 2, 1]})

    with st.expander("Expander"):
        st.write('Some text')
        st.code('... and more')

st.divider()

with st.container():
    with st.popover("popover"):
        st.markdown("some text")
        name = st.text_input("What's your name?")
        red = st.checkbox("Show red items.", True)

    st.write("Your name:", name)
    if red:
        st.write(":red[This is a red item.]")

st.divider()
st.caption("some footnote")
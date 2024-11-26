import streamlit as st

st.set_page_config(page_title="Snipper", page_icon="🔥")

from src.password import check_password


if not check_password():
    st.stop()  # Do not continue if check_password is not True.


# Main Streamlit app starts here
st.title('Title')
st.subheader('v0.0.1')


pg = st.navigation(
    pages=[
        st.Page("pages/hello_world.py", title="HelloWord", icon=":material/thumb_up:", default=True),
        st.Page("pages/forms.py", title="Forms", icon="📝"),
        st.Page("pages/chat.py", title="Chat", icon="💬"),
    ],
    # position="sidebar",
    # expanded=True,
)

pg.run()
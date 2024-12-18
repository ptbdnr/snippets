import streamlit as st

st.set_page_config(page_title="Snippets", page_icon="🔥")

from password import check_password


if not check_password(f):
    st.stop()  # Do not continue if check_password is not True.


# Main Streamlit app starts here
st.logo(image='media/Smiley.svg.png', size='medium', link='https://en.wikipedia.org/wiki/Smiley')
st.title('Title')
st.subheader('v0.0.1')


pg = st.navigation(
    pages=[
        st.Page("pages/hello_world.py", title="HelloWord", icon=":material/thumb_up:", default=True),
        st.Page("pages/forms.py", title="Forms", icon="📝"),
        st.Page("pages/chat.py", title="Chat", icon="💬"),
        st.Page("pages/layout.py", title="Layout", icon="📊"),
    ],
    # position="sidebar",
    # expanded=True,
)

pg.run()

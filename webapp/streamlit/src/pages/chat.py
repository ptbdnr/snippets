import time

import streamlit as st


_LOREM_IPSUM = """
This is formatted: **bold**, _italic_, and `code`. This is a [link](https://www.streamlit.io).

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam eu est quis turpis mattis aliquam a non justo. Sed libero nibh, lacinia dignissim tincidunt vel, congue vel erat. Pellentesque porta augue ac diam convallis, malesuada lacinia mi ultricies. Maecenas sodales odio vel lacinia pellentesque. Vivamus erat sapien, feugiat vitae orci euismod, accumsan imperdiet est. Nulla tempor erat mattis, mollis quam a, pellentesque magna. Cras lectus est, luctus non nisl nec, eleifend dictum risus. Aenean vestibulum posuere est, a ultricies ex consectetur nec. Nullam quis tempus diam. Quisque semper et sapien ac mollis. Nullam viverra risus a scelerisque imperdiet.

Vivamus eleifend scelerisque augue vitae egestas. Phasellus auctor nisi in lacus volutpat, id commodo leo auctor. Donec sit amet nisl nec leo pretium sollicitudin et sit amet risus. Sed in nisl eget nibh pretium vehicula in vel felis. Nunc ut scelerisque tortor, eu gravida diam. In hac habitasse platea dictumst. Nulla facilisi. Nam at augue nec velit laoreet rhoncus. Proin consectetur semper vulputate.
"""


def stream_data():
    for word in _LOREM_IPSUM.split(" "):
        yield word + " "
        time.sleep(0.02)


prompt = st.chat_input("Say something")
if prompt:
    with st.chat_message(name="user", avatar="🦄"):
        st.write(prompt)
    with st.chat_message(name="assistant", avatar="🤖"):
        with st.status(label="Backend task"):
            st.write("doing", prompt)
            time.sleep(2)
            st.write("done", prompt)
        st.write_stream(stream_data)

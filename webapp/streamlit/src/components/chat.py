import time
import logging

import streamlit as st

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.formatter = logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger.addHandler(handler)

STREAM = True

_LOREM_IPSUM = """
This is formatted: **bold**, _italic_, and `code`. This is a [link](https://www.streamlit.io).

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam eu est quis turpis mattis aliquam a non justo. Sed libero nibh, lacinia dignissim tincidunt vel, congue vel erat. Pellentesque porta augue ac diam convallis, malesuada lacinia mi ultricies. Maecenas sodales odio vel lacinia pellentesque. Vivamus erat sapien, feugiat vitae orci euismod, accumsan imperdiet est. Nulla tempor erat mattis, mollis quam a, pellentesque magna. Cras lectus est, luctus non nisl nec, eleifend dictum risus. Aenean vestibulum posuere est, a ultricies ex consectetur nec. Nullam quis tempus diam. Quisque semper et sapien ac mollis. Nullam viverra risus a scelerisque imperdiet.

Vivamus eleifend scelerisque augue vitae egestas. Phasellus auctor nisi in lacus volutpat, id commodo leo auctor. Donec sit amet nisl nec leo pretium sollicitudin et sit amet risus. Sed in nisl eget nibh pretium vehicula in vel felis. Nunc ut scelerisque tortor, eu gravida diam. In hac habitasse platea dictumst. Nulla facilisi. Nam at augue nec velit laoreet rhoncus. Proin consectetur semper vulputate.
"""

class AIMessage:
    content: str

    def __init__(self, content: str) -> None:
        self.content = content


def generate_response(messages) -> str:
    """Generate a response."""
    return AIMessage(content=_LOREM_IPSUM)

def stream_response(messages) -> str:
    """Stream a response content."""
    for word in _LOREM_IPSUM.split(" "):
        yield word + " "
        time.sleep(0.02)

def component() -> None:
    """Render component for the tab."""

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Say something..."):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display assistant response in chat message container
    with st.chat_message(name="assistant"):
        with st.status(label="Backend task"):
            st.write("doing", prompt)
            time.sleep(0.5)
            st.write("done", prompt)
        if STREAM:
            response = st.write_stream(stream_response(messages=st.session_state.messages))
        else:
            ai_message = generate_response(messages=st.session_state.messages)
            logger.debug(f"AI message: {ai_message}")
            response = ai_message.content
            st.markdown(response)
        
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

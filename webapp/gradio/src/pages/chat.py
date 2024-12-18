import time

import gradio as gr


_LOREM_IPSUM = """
This is formatted: **bold**, _italic_, and `code`. This is a [link](https://www.streamlit.io).

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam eu est quis turpis mattis aliquam a non justo. Sed libero nibh, lacinia dignissim tincidunt vel, congue vel erat. Pellentesque porta augue ac diam convallis, malesuada lacinia mi ultricies. Maecenas sodales odio vel lacinia pellentesque. Vivamus erat sapien, feugiat vitae orci euismod, accumsan imperdiet est. Nulla tempor erat mattis, mollis quam a, pellentesque magna. Cras lectus est, luctus non nisl nec, eleifend dictum risus. Aenean vestibulum posuere est, a ultricies ex consectetur nec. Nullam quis tempus diam. Quisque semper et sapien ac mollis. Nullam viverra risus a scelerisque imperdiet.

Vivamus eleifend scelerisque augue vitae egestas. Phasellus auctor nisi in lacus volutpat, id commodo leo auctor. Donec sit amet nisl nec leo pretium sollicitudin et sit amet risus. Sed in nisl eget nibh pretium vehicula in vel felis. Nunc ut scelerisque tortor, eu gravida diam. In hac habitasse platea dictumst. Nulla facilisi. Nam at augue nec velit laoreet rhoncus. Proin consectetur semper vulputate.
"""

with gr.Blocks() as app:

    def user(user_message, history: list):
        return "", history + [{"role": "user", "content": user_message}]

    def bot(history: list):
        bot_message = _LOREM_IPSUM
        # tool use
        user_msg_content = history[-1]['content']
        history.append(
            gr.ChatMessage(
                    role="assistant",
                    content=f"doing {user_msg_content}",
                    metadata={"title": "Backend task"},
                )
        )
        yield history
        time.sleep(2)
        history.append(
            gr.ChatMessage(
                    role="assistant",
                    content=f"done {user_msg_content}"
                )
        )
        yield history
        # message
        history.append({"role": "assistant", "content": ""})
        for character in bot_message:
            history[-1]['content'] += character
            time.sleep(0.01)
            yield history

    def like(evt: gr.LikeData):
        if evt.liked:
            gr.Info("User liked", duration=3)
        else:
            gr.Warning("User disliked", duration=3)
        print(f"log: user {'' if evt.liked else 'dis'}liked")
        print(evt.index, evt.liked, evt.value)


    chatbot = gr.Chatbot(type="messages", show_copy_button=True)
    chatbot.like(like)
    prompt_textbox = gr.Textbox(placeholder="Say something", show_label=False)

    prompt_textbox.submit(user, [prompt_textbox, chatbot], [prompt_textbox, chatbot], queue=False).then(
        bot, chatbot, chatbot
    )


if __name__ == "__main__":
    app.launch(share=False, server_name="0.0.0.0")
    # If share=True, then it attempts to create a link like
    # https://**********.gradio.live

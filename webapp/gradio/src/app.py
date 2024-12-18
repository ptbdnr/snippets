import gradio as gr

from password import credentials

from pages.hello_world import app as hello_world_app
from pages.forms import app as forms_app
from pages.chat import app as chat_app
from pages.layout import app as layout_app



with gr.Blocks() as app:
    # not working, see: https://github.com/gradio-app/gradio/issues/1997
    gr.Markdown("![markup image around here](file/media/Smiley.svg.png)")
    gr.Markdown("# Title")
    gr.HTML("<code>v0.0.1</code>")

    with gr.Tab(label="Hello World"):
        hello_world_app.render()
    with gr.Tab(label="📝 Forms"):
        forms_app.render()
    with gr.Tab(label="💬 Chat"):
        chat_app.render()
    with gr.Tab(label="📊 Layout"):
        layout_app.render()


if __name__ == "__main__":
    app.launch(
        share=False, 
        server_name="0.0.0.0", 
        allowed_paths=['/', '/media/'],
        auth=credentials
    )
    # If share=True, then it attempts to create a link like
    # https://**********.gradio.live
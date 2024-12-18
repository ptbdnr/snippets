import gradio as gr

with gr.Blocks() as app:
    # not working, see: https://github.com/gradio-app/gradio/issues/1997
    gr.Markdown("# Hello World")

    button=gr.Button("Click me", variant="primary")

    def click_handler() -> str:
        gr.Info("You clicked the button!", duration=3)
        return """<a href="https://www.wikipedia.org/" target="_blank">wikipedia</a>"""

    button.click(
        fn=click_handler,
        inputs=None,
        outputs=gr.HTML(show_label=False)
    )


if __name__ == "__main__":
    app.launch(share=False, server_name="0.0.0.0", allowed_paths=['/', '/media/'])
    # If share=True, then it attempts to create a link like
    # https://**********.gradio.live

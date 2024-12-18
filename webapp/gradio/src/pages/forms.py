import gradio as gr

with gr.Blocks() as app:

    with gr.Column(elem_id='output D', visible=False) as out_d_col:
            out_d_html = gr.HTML(show_label=False)
            out_d_textbox = gr.Textbox(lines=1, show_label=False)
            out_d_matrix = gr.Matrix()

    with gr.Group(elem_id='simple form') as group1:
        with gr.Column() as col:
            dropdown = gr.Dropdown(
                choices=['A', 'B'], 
                value='A', 
                label="select one"
            )
            input_textbox = gr.Textbox(
                lines=3, 
                label="text area"
            )
            button=gr.Button(value="Submit")

            with gr.Column(visible=False) as output_col:
                out_markdown = gr.Markdown("Output")
                out_textbox = gr.Textbox(lines=1, show_label=False)

            def button_click_handler(textbox_input: str, dropdown_input: str) -> str:
                gr.Info("start processing", duration=3)
                return {
                    output_col: gr.Column(visible=True),
                    out_markdown: "Output",
                    out_textbox: f"input: {textbox_input} {dropdown_input}",
                }

            button.click(
                fn=button_click_handler,
                inputs=[input_textbox, dropdown],
                outputs=[out_markdown, out_textbox, output_col]
            )

    with gr.Group(elem_id='A-B button columns') as group2:
        with gr.Row() as row:
            
            with gr.Column() as col1:
                button=gr.Button(value="button A")

                def button_click_handler() -> str:
                    gr.Info("pressed button a", duration=3)
                    return [
                        '<h1>A list</h1>',
                        'A list',
                        [[x*y for x in range(1,4)] for y in range(1,3)]
                    ]

                button.click(
                    fn=button_click_handler,
                    inputs=[],
                    outputs=[
                        gr.HTML(show_label=False),
                        gr.Textbox(lines=1, show_label=False),
                        gr.Matrix()
                    ]
                )

            with gr.Column() as col2:
                button=gr.Button(value="button B")

                def button_click_handler() -> str:
                    gr.Info("pressed button b", duration=3)
                    return [
                        '<h1>B list</h1>',
                        'B list',
                        [[x*y for x in range(1,4)] for y in range(1,3)]
                    ]

                button.click(
                    fn=button_click_handler,
                    inputs=[],
                    outputs=[
                        gr.HTML(show_label=False),
                        gr.Textbox(lines=1, show_label=False),
                        gr.Matrix()
                    ]
                )

    # button D
    button=gr.Button(value="button D")

    def button_click_handler() -> str:
        gr.Info("pressed button D", duration=3)
        return {
            out_d_col: gr.Column(visible=True),
            out_d_html: '<h1>D list</h1>',
            out_d_textbox: 'D list',
            out_d_matrix: [[x*y for x in range(1,4)] for y in range(1,3)],
        }

    button.click(
        fn=button_click_handler,
        inputs=[],
        outputs=[out_d_html, out_d_textbox, out_d_matrix, out_d_col]
    )


if __name__ == "__main__":
    app.launch(share=False, server_name="0.0.0.0")
    # If share=True, then it attempts to create a link like
    # https://**********.gradio.live

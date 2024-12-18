import json

import gradio as gr

with gr.Blocks() as app:

    with gr.Tab(label="Tab1"):
        gr.HTML("<h1>Tab1</h1>")
        gr.Markdown("Some text")
    with gr.Tab(label="Tab2"):
        gr.HTML("<h1>Tab2</h1>")
        gr.Markdown("Some text")
    
    with gr.Blocks() as two_col_block:
        with gr.Row() as two_cols:
            with gr.Column() as col1:
                gr.Markdown("# Column1")
                gr.Markdown("Some text")
            with gr.Column() as col2:
                gr.Markdown("# Column2")
                gr.Markdown("Some text")

    with gr.Group() as plot:
        class DummyData:
            def __init__(self, vals):
                self.vals = vals
            
            def __getattr__(self, item: str):
                if item == 'dtype': return 'int'

        class DummyDataFrame:
            columns = ['x', 'y']
            vals = {
                'x': DummyData(vals=[x for x in range(1,7)]),
                'y': DummyData(vals=[1, 5, 2, 6, 2, 1])
            }

            def to_json(self, **kwargs) -> str:
                """Convert the object to a JSON string."""
                ans = {'columns': self.columns}
                [ans.update({k: v.vals}) for k, v in self.vals.items()]
                data = [[self.vals['x'].vals[i], self.vals['y'].vals[i]] for i in range(6)]
                ans['data'] = data
                return json.dumps(ans)

            def __getitem__(self, item: str):
                return self.vals[item]

        gr.BarPlot(value=DummyDataFrame(), x="x", y="y")
        
    with gr.Accordion(label="Expander", open=False):
        gr.Markdown("Some text")
        gr.Code(value="... and more", lines=1)


if __name__ == "__main__":
    app.launch(share=False, server_name="0.0.0.0")
    # If share=True, then it attempts to create a link like
    # https://**********.gradio.live
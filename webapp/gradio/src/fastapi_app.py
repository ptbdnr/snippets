from fastapi import FastAPI
from fastapi.responses import HTMLResponse

import gradio as gr

from pages.hello_world import app as hello_world_app
from pages.forms import app as forms_app
from pages.chat import app as chat_app
from pages.layout import app as layout_app

app = FastAPI()

route_map = {
    "HelloWorld": "/pages/hello_world",
    "Forms": "/pages/forms",
    "Chat": "/pages/chat",
    "Layout": "/pages/layout",
}
iframe_dimensions = "height=300px width=1000px"

index_html = f"""
![markup image around here](file/Smiley.svg.png)
<h1>Title</h1>
<h2>v0.0.1</h2>
<div>
<iframe src={route_map['HelloWorld']} {iframe_dimensions}></iframe>
<iframe src={route_map['Forms']} {iframe_dimensions}></iframe>
<iframe src={route_map['Chat']} {iframe_dimensions}></iframe>
<iframe src={route_map['Layout']} {iframe_dimensions}></iframe>
</div>
"""

@app.get("/", response_class=HTMLResponse)
def index():
    return index_html


app = gr.mount_gradio_app(app, hello_world_app, path=route_map['HelloWorld'])
app = gr.mount_gradio_app(app, forms_app, path=route_map['Forms'])
app = gr.mount_gradio_app(app, chat_app, path=route_map['Chat'])
app = gr.mount_gradio_app(app, layout_app, path=route_map['Layout'])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)

from typing import Annotated, Callable

from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from src.pages.chat import router as router_chat
from src.pages.forms import router as router_forms
from src.pages.hello_world import router as router_hello_world
from src.pages.layout import router as router_layout

app = FastAPI()
app.include_router(router_hello_world)
app.include_router(router_forms)
app.include_router(router_chat)
app.include_router(router_layout)

route_map = {
    "Hello World": {"path": "/hello_world"},
    "Forms": {"path": "/forms"},
    "Chat": {"path": "/chat"},
    "Layout": {"path": "/layout"},
}

links = "\n".join([f"""<li><a href="{v['path']}">{k}</a></li>""" for (k,v) in route_map.items()])

index_html = f"""
![markup image around here](file/Smiley.svg.png)
<h1>Title</h1>
<h2>v0.0.1</h2>
<ul>
    {links}
</ul>
"""

@app.get("/", response_class=HTMLResponse)
async def index():
    return index_html

# Data API
mockup_items = [
    {"id": 1, "key1": "id1_key1", "key2": "id1_key2"},
    {"id": 2, "key1": "id2_key1", "key2": "id2_key2"},
    {"id": 3, "key1": "id3_key1", "key2": "id3_key2"},
]

@app.get("/api", response_class=JSONResponse)
async def read_items():
    return mockup_items

@app.get("/api/{item_id}", response_class=JSONResponse)
async def read_item(item_id: int, attribute_name: str | None = None):
    selected_items = [item for item in mockup_items if item["id"] == item_id]
    selected_item = selected_items[0] if selected_items else None
    if not selected_item:
        return JSONResponse(status_code=404, content={"message": "Item not found"})
    elif not attribute_name:
        return selected_item
    elif attribute_name in selected_item:
        return {"id": selected_item["id"], attribute_name: selected_item[attribute_name]}
    else:
        return JSONResponse(status_code=404, content={"message": "Attribute not found"})

@app.get("/api/{item_id}/attributes/{attribute_name}", response_class=JSONResponse)
async def read_item_attribute(item_id: int, attribute_name: str):
    selected_items = [item for item in mockup_items if item["id"] == item_id]
    selected_item = selected_items[0] if selected_items else None
    if not selected_item:
        return JSONResponse(status_code=404, content={"message": "Item not found"})
    elif attribute_name in selected_item:
        return {"id": selected_item["id"], attribute_name: selected_item[attribute_name]}
    else:
        return JSONResponse(status_code=404, content={"message": "Attribute not found"})

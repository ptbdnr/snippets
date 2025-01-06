from __future__ import annotations

from flask import Blueprint, Flask, jsonify, url_for

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/", methods=["GET"])
def index() -> str:
    """Render the index page with links to other pages."""
    route_map = {
        "Hello World": {"path": "/hello_world"},
        "Forms": {"path": "/forms"},
        "Chat": {"path": "/chat"},
        "Layout": {"path": "/layout"},
    }
    links = "\n".join([f"""<li><a href="{v['path']}">{k}</a></li>""" for (k, v) in route_map.items()])
    index_html = f"""
    <img src="{url_for(endpoint="static", filename="Smiley.svg.png")}" width="40" height="40"/>
    <h1>Title</h1>
    <h2>v0.0.1</h2>
    <ul>
        {links}
    </ul>
    """
    return index_html


hello_world_page = Blueprint("hello_world_page", __name__, template_folder="templates")
@hello_world_page.route("/hello_world", methods=["GET", "POST"])
def hello_world_index() -> str:
    from src.pages.hello_world import index
    return index()
app.register_blueprint(hello_world_page)

forms_page = Blueprint("forms_page", __name__, template_folder="templates")
@forms_page.route("/forms", methods=["GET", "POST"])
def forms_index() -> str:
    from src.pages.forms import index
    return index()
app.register_blueprint(forms_page)

chat_page = Blueprint("chat_page", __name__, template_folder="templates")
@chat_page.route("/chat", methods=["GET", "POST"])
def chat_index() -> str:
    from src.pages.chat import index
    return index()
app.register_blueprint(chat_page)

layout_page = Blueprint("layout_page", __name__, template_folder="templates")
@layout_page.route("/layout", methods=["GET"])
def layout_index() -> str:
    from src.pages.layout import index
    return index()
app.register_blueprint(layout_page)


# Data API
mockup_items = [
    {"id": 1, "key1": "id1_key1", "key2": "id1_key2"},
    {"id": 2, "key1": "id2_key1", "key2": "id2_key2"},
    {"id": 3, "key1": "id3_key1", "key2": "id3_key2"},
]

@app.route("/api", methods=["GET"])
def read_items() -> str:
    return jsonify(mockup_items)

@app.route("/api/<int:item_id>", methods=["GET"])
def read_item(item_id: int) -> str:
    selected_items = [item for item in mockup_items if item["id"] == item_id]
    selected_item = selected_items[0] if selected_items else None
    if not selected_item:
        return jsonify({"message": "Item not found"}), 404
    return jsonify(selected_item)

@app.route("/api/<int:item_id>/attributes/<attribute_name>", methods=["GET"])
def read_item_attribute(item_id: int, attribute_name: str | None = None) -> str:
    selected_items = [item for item in mockup_items if item["id"] == item_id]
    selected_item = selected_items[0] if selected_items else None
    if not selected_item:
        return jsonify({"message": "Item not found"}), 404
    if attribute_name in selected_item:
        return jsonify({"id": selected_item["id"], attribute_name: selected_item[attribute_name]})
    return jsonify({"message": "Attribute not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)

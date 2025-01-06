import time

from flask import Flask, Response, render_template, request

_LOREM_IPSUM = """
This is formatted: **bold**, _italic_, and `code`. This is a [link](https://www.streamlit.io).

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam eu est quis turpis mattis aliquam a non justo. Sed libero nibh, lacinia dignissim tincidunt vel, congue vel erat. Pellentesque porta augue ac diam convallis, malesuada lacinia mi ultricies. Maecenas sodales odio vel lacinia pellentesque. Vivamus erat sapien, feugiat vitae orci euismod, accumsan imperdiet est. Nulla tempor erat mattis, mollis quam a, pellentesque magna. Cras lectus est, luctus non nisl nec, eleifend dictum risus. Aenean vestibulum posuere est, a ultricies ex consectetur nec. Nullam quis tempus diam. Quisque semper et sapien ac mollis. Nullam viverra risus a scelerisque imperdiet.

Vivamus eleifend scelerisque augue vitae egestas. Phasellus auctor nisi in lacus volutpat, id commodo leo auctor. Donec sit amet nisl nec leo pretium sollicitudin et sit amet risus. Sed in nisl eget nibh pretium vehicula in vel felis. Nunc ut scelerisque tortor, eu gravida diam. In hac habitasse platea dictumst. Nulla facilisi. Nam at augue nec velit laoreet rhoncus. Proin consectetur semper vulputate.
"""

app = Flask(__name__, template_folder="./src/templates")

history = []

def bot(history: list):
    bot_message = _LOREM_IPSUM
    history.append({"role": "assistant", "content": ""})
    for character in bot_message:
        history[-1]["content"] += character
        time.sleep(0.001)
        yield character

@app.route("/", methods=["GET", "POST"])
def index() -> str:
    if request.method == "GET":
        return render_template("chat.html")
    if request.method == "POST":
        form_data = request.form["value"]
        history.append({"role": "user", "content": form_data})
        return Response(bot(history=history), content_type="text/event-stream")
    msg = "Method not supported"
    raise ValueError(msg)

if __name__ == "__main__":
    app.run()

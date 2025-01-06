from flask import Flask, jsonify, render_template, request
from pydantic import BaseModel

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/", methods=["GET", "POST"])
def index() -> str:
    if request.method == "GET":
        return render_template("forms.html")
    if request.method == "POST":
        form_id = request.form.get("form_id")
        letter = request.form.get("letter")
        message = request.form.get("message")
        print(str(request), form_id, letter, message)

        context = {}
        if form_id == "form_1":
            context = {"result": {"label": "output", "content": f"{letter!s} {message!s}"}}
        elif form_id == "form_4":
            context = {"resultD": {"label": "D list", "content": "d list"}}

        return render_template("forms.html", **context)
    msg = "Method not supported"
    raise ValueError(msg)

class FormData(BaseModel):
    value: str

@app.route("/AB/", methods=["POST"])
def post_ab_handler(body: FormData) -> str:
    if body.value == "A":
        return jsonify({"resultAB": {"label": "A list", "content": "a list"}})
    if body.value == "B":
        return jsonify({"resultAB": {"label": "B list", "content": "b list"}})
    msg = "Invalid value"
    raise ValueError(msg)

if __name__ == "__main__":
    app.run(debug=True)

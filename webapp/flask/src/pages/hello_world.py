from flask import Blueprint, Flask, render_template, request

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/", methods=["GET", "POST"])
def index() -> str:
    if request.method == "GET":
        return render_template("hello_world.html")
    if request.method == "POST":
        return render_template(
            "hello_world.html",
            result={"link": "https://www.wikipedia.org", "label": "wikipedia"},
        )
    msg = "Method not supported"
    raise ValueError(msg)


if __name__ == "__main__":
    app.run(debug=True)

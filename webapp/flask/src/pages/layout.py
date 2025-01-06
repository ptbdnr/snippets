from flask import Flask, render_template, request

app = Flask(__name__, template_folder="./src/templates")

@app.route("/", methods=["GET"])
def index() -> str:
    if request.method == "GET":
        return render_template("layout.html")
    msg = "Method not supported"
    raise ValueError(msg)

if __name__ == "__main__":
    app.run()

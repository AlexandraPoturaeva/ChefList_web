import os

from flask import Flask, abort


app = Flask(__name__)


@app.route("/")
def index():
    try:
        with open(
            os.path.join("html", "index.html"), "r", encoding="utf-8"
        ) as page_file:
            page_text = page_file.read()
            return page_text
    except FileNotFoundError:
        abort(404)


if __name__ == "__main__":
    app.run(debug=True)

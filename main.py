from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/learn/python")
def learn_python():
    return render_template("python.html")


@app.route("/docs/python")
@app.route("/docs/python")
def python_catalog():
    topics = [
        {
            "title": "Variables",
            "description": "Learn how variables store data in Python.",
            "available": False,
        },
        {
            "title": "Conditions",
            "description": "Learn how to make decisions using if statements.",
            "available": False,
        },
        {
            "title": "Loops",
            "description": "Learn how to repeat actions using loops.",
            "available": False,
        },
        {
            "title": "Functions",
            "description": "Learn how to define and call functions.",
            "available": True,
        },
    ]

    return render_template(
        "python_catalog.html",
        topics=topics,
    )


if __name__ == "__main__":
    app.run(debug=True)

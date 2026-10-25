from datetime import datetime
from flask import Flask, render_template, request, jsonify

from flask_sqlalchemy import SQLAlchemy

import json

from flask_migrate import Migrate

import re

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Words(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english = db.Column(db.String(255), nullable=False)
    russian = db.Column(db.String(255), nullable=False)
    transcription = db.Column(db.String(255))


class Documents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    source = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


def extract_words(text):
    words = re.findall(r"\b[a-zA-Z]+\b", text)
    return words


def translate_text(text):
    words = extract_words(text)
    result = {}

    for word in words:
        translation = Words.query.filter_by(english=word.lower()).first()

        if translation:
            result[word] = translation.russian
        else:
            result[word] = "Перевод не найден"

    return result


@app.route("/")
def home():
    return render_template("main.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/documentation")
def documents_list():
    documents = Documents.query.all()

    return render_template("documents_list.html", documents=documents)


@app.route("/documentation/<int:id>")
def documentation(id):
    document = Documents.query.get(id)

    parts = []

    if document:
        parts = re.split(r"([A-Za-z]+)", document.text)

    return render_template("documentation.html", document=document, parts=parts)


@app.route("/dictionary")
def dictionary():
    return render_template("dictionary.html")


@app.route("/translate", methods=["GET"])
def translate():
    word = request.args.get("word", "").strip()

    if not word:
        return jsonify({"error": "Слово не указано"}), 400

    result = Words.query.filter(db.func.lower(Words.english) == word.lower()).first()

    if result is None:
        return jsonify({"word": word, "translation": None}), 404

    return app.response_class(
        response=json.dumps(
            {
                "word": word,
                "translation": result.russian,
                "transcription": result.transcription,
            },
            ensure_ascii=False,
        ),
        status=200,
        mimetype="application/json",
    )


if __name__ == "__main__":
    app.run()

import json

from pathlib import Path

from app import app, db, Words

json_file_path = Path(__file__).parent / "top10000.json"

with open(json_file_path, "r", encoding="utf-8") as file:
    words_data = json.load(file)

with app.app_context():
    if Words.query.first():
        print("База уже содержит слова. Импорт отменён.")
    else:
        db.session.add_all(
            [
                Words(
                    english=item["word"].strip(),
                    russian=item["translation"].strip(),
                    transcription=item.get("transcription"),
                )
                for item in words_data
            ]
        )

        db.session.commit()
        print(f"Импортировано слов: {len(words_data)}")

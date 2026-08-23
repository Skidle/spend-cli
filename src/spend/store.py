from pathlib import Path
import json

def load(path: Path) -> dict:
    try:
        string = path.read_text(encoding="utf-8")
        return json.loads(string)
    except FileNotFoundError:
        return {"next_id": 1, "expenses": []}

def save(path: Path, data: dict) -> None:
    string = json.dumps(data, indent=2)
    path.write_text(string, encoding="utf-8")

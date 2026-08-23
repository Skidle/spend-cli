from pathlib import Path
import json

def load(path: Path) -> list[dict]:
    try:
        string = path.read_text(encoding="utf-8")
        return json.loads(string)
    except FileNotFoundError:
        return []

def save(path: Path, expenses: list[dict]) -> None:
    string = json.dumps(expenses, indent=2)
    path.write_text(string, encoding="utf-8")

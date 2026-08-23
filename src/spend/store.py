import json
from pathlib import Path
from typing import Any


def load(path: Path) -> dict[str, Any]:
    try:
        string = path.read_text(encoding="utf-8")
        data: dict[str, Any] = json.loads(string)
        return data
    except FileNotFoundError:
        return {"next_id": 1, "expenses": []}
    except json.JSONDecodeError as err:
        raise ValueError(f"The store at {path} is corrupt.") from err

def save(path: Path, data: dict[str, Any]) -> None:
    string = json.dumps(data, indent=2)
    path.write_text(string, encoding="utf-8")

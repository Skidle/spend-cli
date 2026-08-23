from pathlib import Path
from typing import Any

import pytest

from spend.store import load, save


def test_load_returns_what_save_wrote(tmp_path: Path) -> None:
    expenses: list[dict[str, Any]] = [
        {"id": 1, "amount": 3, "category": "food"},
        {"id": 2, "amount": 10.5, "category": "transport"},
    ]
    data: dict[str, Any] = {"next_id": 3, "expenses": expenses}

    path = tmp_path / ".spend.json"
    save(path, data)

    result = load(path)
    assert result == data

def test_load_returns_empty_document_when_file_missing(tmp_path: Path) -> None:
    path = tmp_path / ".spend.json"
    result = load(path)
    assert result == {"next_id": 1, "expenses": []}

def test_load_raises_for_a_corrupt_store(tmp_path: Path) -> None:
    path = tmp_path / ".spend.json"
    path.write_text("garbage")

    with pytest.raises(ValueError, match="corrupt"):
        load(path)

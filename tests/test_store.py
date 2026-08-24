from pathlib import Path

import pytest

from spend.models import Expense, Ledger
from spend.store import load, save


def test_load_returns_what_save_wrote(tmp_path: Path) -> None:
    expenses = [
        Expense(id=1, amount=3, category="food", date="2026-08-24"),
        Expense(id=2, amount=10.5, category="transport", date="2026-08-25"),
    ]
    data = Ledger(next_id=3, expenses=expenses)

    path = tmp_path / ".spend.json"
    save(path, data)

    result = load(path)
    assert result == data

def test_load_returns_empty_document_when_file_missing(tmp_path: Path) -> None:
    path = tmp_path / ".spend.json"
    result = load(path)
    assert result == Ledger()

def test_load_raises_for_a_corrupt_store(tmp_path: Path) -> None:
    path = tmp_path / ".spend.json"
    path.write_text("garbage")

    with pytest.raises(ValueError, match="corrupt"):
        load(path)

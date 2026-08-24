import datetime

import pytest

from spend.commands import add
from spend.models import Expense, Ledger


def test_add_returns_the_created_expense() -> None:
    data = Ledger()

    result = add(data, amount=3.5, category="food", date="2026-08-23")

    assert result.id == 1
    assert result.amount == 3.5
    assert result.category == "food"
    assert result.date == "2026-08-23"
    assert result.note is None

def test_add_appends_to_the_list() -> None:
    data = Ledger(
        next_id=3,
        expenses=[
            Expense(id=1, amount=3, category="food", date="2026-08-24"),
            Expense(id=2, amount=10.5, category="transport", date="2026-08-25"),
        ]
    )

    result = add(data, amount=23.7, category="entertainment")

    assert data.expenses[-1] == result
    assert len(data.expenses) == 3
    assert data.next_id == 4

def test_add_ids_increment() -> None:
    data = Ledger()

    result = add(data, amount=3.5, category="food")

    assert result.id == 1

    result = add(data, amount=3.5, category="food")

    assert result.id == 2

def test_add_date_defaults_to_today() -> None:
    data = Ledger()

    result = add(data, amount=3.5, category="food")

    assert result.date == datetime.datetime.now(tz=datetime.UTC).date().isoformat()

def test_add_does_not_reuse_ids_after_remove() -> None:
    data = Ledger(
        next_id=3,
        expenses=[
            Expense(id=1, amount=3, category="food", date="2026-08-24"),
            Expense(id=2, amount=10.5, category="transport", date="2026-08-25"),
        ]
    )

    del data.expenses[1]

    result = add(data, amount=3.5, category="food")

    assert data.expenses[-1] == result
    assert data.expenses[-1].id == 3
    assert data.next_id == 4

def test_add_rejects_a_non_positive_amount() -> None:
    data = Ledger()

    with pytest.raises(ValueError, match="positive"):
        add(data, amount=0, category="food")

def test_add_rejects_a_malformed_date() -> None:
    data = Ledger()

    with pytest.raises(ValueError, match="valid ISO date"):
        add(data, amount=4, category="food", date="garbage")

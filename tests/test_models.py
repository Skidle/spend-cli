from dataclasses import FrozenInstanceError

import pytest

from spend.models import Expense


def test_round_trip() -> None:
    e = Expense(id=1, amount=12.5, category="food", date="2026-08-24", note="milk")
    assert Expense.from_dict(e.to_dict()) == e

def test_expense_is_frozen() -> None:
    e = Expense(id=1, amount=12.5, category="food", date="2026-08-24")
    with pytest.raises(FrozenInstanceError):
        e.amount = 20   # type: ignore[misc]

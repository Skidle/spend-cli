import datetime
import pytest

from spend.commands import add

def test_add_returns_the_created_expense():
    data = {"next_id": 1, "expenses": []}

    result = add(data, amount=3.5, category="food", date="2026-08-23")

    assert result["id"] == 1
    assert result["amount"] == 3.5
    assert result["category"] == "food"
    assert result["date"] == "2026-08-23"
    assert result["note"] is None

def test_add_appends_to_the_list():
    data = {
        "next_id": 3,
        "expenses": [
            {"id": 1, "amount": 3, "category": "food"},
            {"id": 2, "amount": 10.5, "category": "transport"},
        ]
    }

    result = add(data, amount=23.7, category="entertainment")

    assert data["expenses"][-1] == result
    assert len(data["expenses"]) == 3
    assert data["next_id"] == 4

def test_add_ids_increment():
    data = {"next_id": 1, "expenses": []}

    result = add(data, amount=3.5, category="food")

    assert result["id"] == 1

    result = add(data, amount=3.5, category="food")

    assert result["id"] == 2

def test_add_date_defaults_to_today():
    data = {"next_id": 1, "expenses": []}

    result = add(data, amount=3.5, category="food")

    assert result["date"] == datetime.date.today().isoformat()

def test_add_does_not_reuse_ids_after_remove():
    data = {
        "next_id": 3,
        "expenses": [
            {"id": 1, "amount": 3, "category": "food"},
            {"id": 2, "amount": 10.5, "category": "transport"},
        ]
    }

    del data["expenses"][1]

    result = add(data, amount=3.5, category="food")

    assert data["expenses"][-1] == result
    assert data["expenses"][-1]["id"] == 3
    assert data["next_id"] == 4

def test_add_rejects_a_non_positive_amount():
    data = {"next_id": 1, "expenses": []}

    with pytest.raises(ValueError, match="positive"):
        add(data, amount=0, category="food")

def test_add_rejects_a_malformed_date():
    data = {"next_id": 1, "expenses": []}

    with pytest.raises(ValueError, match="valid ISO date"):
        add(data, amount=4, category="food", date="garbage")

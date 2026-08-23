import datetime

from spend.commands import add

def test_add_returns_the_created_expense():
    expenses = []
    result = add(expenses, amount=3.5, category="food", date="2026-08-23")
    assert result["id"] == 1
    assert result["amount"] == 3.5
    assert result["category"] == "food"
    assert result["date"] == "2026-08-23"
    assert result["note"] is None

def test_add_appends_to_the_list():
    expenses = [
        {"id": 1, "amount": 3, "category": "food"},
        {"id": 2, "amount": 10.5, "category": "transport"},
    ]

    result = add(expenses, amount=23.7, category="entertainment")
    assert expenses[-1] == result
    assert len(expenses) == 3

def test_add_ids_increment():
    expenses = []
    result = add(expenses, amount=3.5, category="food")
    assert result["id"] == 1

    result = add(expenses, amount=3.5, category="food")
    assert result["id"] == 2

def test_add_date_defaults_to_today():
    expenses = []
    result = add(expenses, amount=3.5, category="food")
    assert result["date"] == datetime.date.today().isoformat()
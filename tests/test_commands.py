import datetime
import pytest
import copy

from spend.commands import add, list_expenses

# tests for add command -----------------------------------------------------------------
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

# tests for list_expenses command -----------------------------------------------------------------

@pytest.fixture
def expenses_list():
    return [
        {"id": 3, "amount": 16, "category": "transport", "date": "2026-08-20"},
        {"id": 1, "amount": 3, "category": "food", "date": "2026-08-20"},
        {"id": 4, "amount": 10.5, "category": "transport", "date": "2026-08-22"},
        {"id": 2, "amount": 27, "category": "food", "date": "2026-08-15"},
    ]

def test_list_returns_all_sorted_by_date_then_id(expenses_list):
    expected = [
        {"id": 2, "amount": 27, "category": "food", "date": "2026-08-15"},
        {"id": 1, "amount": 3, "category": "food", "date": "2026-08-20"},
        {"id": 3, "amount": 16, "category": "transport", "date": "2026-08-20"},
        {"id": 4, "amount": 10.5, "category": "transport", "date": "2026-08-22"},
    ]

    result = list_expenses(expenses_list)
    assert result == expected

def test_list_filters_by_category(expenses_list):
    expected = [
        {"id": 2, "amount": 27, "category": "food", "date": "2026-08-15"},
        {"id": 1, "amount": 3, "category": "food", "date": "2026-08-20"},
    ]

    result = list_expenses(expenses_list, category="food")
    assert result == expected

def test_list_filters_by_since_is_inclusive(expenses_list):
    expected = [
        {"id": 1, "amount": 3, "category": "food", "date": "2026-08-20"},
        {"id": 3, "amount": 16, "category": "transport", "date": "2026-08-20"},
        {"id": 4, "amount": 10.5, "category": "transport", "date": "2026-08-22"},
    ]

    result = list_expenses(expenses_list, since="2026-08-20")
    assert result == expected

def test_list_applies_both_category_and_since_filters(expenses_list):
    expected = [
        {"id": 3, "amount": 16, "category": "transport", "date": "2026-08-20"},
        {"id": 4, "amount": 10.5, "category": "transport", "date": "2026-08-22"},
    ]

    result = list_expenses(expenses_list, category="transport", since="2026-08-20")
    assert result == expected

def test_list_does_not_mutate_the_input(expenses_list):
    expenses = copy.deepcopy(expenses_list)

    list_expenses(expenses_list)
    assert expenses == expenses_list

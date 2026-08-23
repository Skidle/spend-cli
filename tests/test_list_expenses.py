import pytest
import copy

from spend.commands import list_expenses

@pytest.fixture
def expenses_list():
    return [
        {"id": 3, "amount": 16, "category": "transport", "date": "2026-08-20"},
        {"id": 1, "amount": 3, "category": "food", "date": "2026-08-20"},
        {"id": 4, "amount": 10.5, "category": "transport", "date": "2026-08-22"},
        {"id": 2, "amount": 27, "category": "food", "date": "2026-08-15"},
    ]

def test_list_expenses_returns_all_sorted_by_date_then_id(expenses_list):
    expected = [
        {"id": 2, "amount": 27, "category": "food", "date": "2026-08-15"},
        {"id": 1, "amount": 3, "category": "food", "date": "2026-08-20"},
        {"id": 3, "amount": 16, "category": "transport", "date": "2026-08-20"},
        {"id": 4, "amount": 10.5, "category": "transport", "date": "2026-08-22"},
    ]

    result = list_expenses(expenses_list)
    assert result == expected

def test_list_expenses_filters_by_category(expenses_list):
    expected = [
        {"id": 2, "amount": 27, "category": "food", "date": "2026-08-15"},
        {"id": 1, "amount": 3, "category": "food", "date": "2026-08-20"},
    ]

    result = list_expenses(expenses_list, category="food")
    assert result == expected

def test_list_expenses_filters_by_since_is_inclusive(expenses_list):
    expected = [
        {"id": 1, "amount": 3, "category": "food", "date": "2026-08-20"},
        {"id": 3, "amount": 16, "category": "transport", "date": "2026-08-20"},
        {"id": 4, "amount": 10.5, "category": "transport", "date": "2026-08-22"},
    ]

    result = list_expenses(expenses_list, since="2026-08-20")
    assert result == expected

def test_list_expenses_applies_both_category_and_since_filters(expenses_list):
    expected = [
        {"id": 3, "amount": 16, "category": "transport", "date": "2026-08-20"},
        {"id": 4, "amount": 10.5, "category": "transport", "date": "2026-08-22"},
    ]

    result = list_expenses(expenses_list, category="transport", since="2026-08-20")
    assert result == expected

def test_list_expenses_does_not_mutate_the_input(expenses_list):
    expenses = copy.deepcopy(expenses_list)

    list_expenses(expenses_list)
    assert expenses == expenses_list

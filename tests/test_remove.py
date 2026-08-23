import pytest

from spend.commands import remove

@pytest.fixture
def expenses_list():
    return [
        {"id": 1, "amount": 30, "category": "food", "date": "2026-08-20"},
        {"id": 3, "amount": 60, "category": "transport", "date": "2026-08-20"},
        {"id": 2, "amount": 10, "category": "food", "date": "2026-08-15"},
    ]

def test_remove_deletes_the_expense(expenses_list):
    expense_id_to_remove = 2
    remove(expenses_list, expense_id=expense_id_to_remove)

    assert 2 not in [e["id"] for e in expenses_list]

def test_remove_returns_the_removed_expense(expenses_list):
    expense_id_to_remove = 2
    removed_expense = remove(expenses_list, expense_id=expense_id_to_remove)

    assert removed_expense["id"] == expense_id_to_remove

def test_remove_leaves_other_expenses_untouched(expenses_list):
    expected = [
        {"id": 1, "amount": 30, "category": "food", "date": "2026-08-20"},
        {"id": 2, "amount": 10, "category": "food", "date": "2026-08-15"},
    ]
    expense_id_to_remove = 3

    remove(expenses_list, expense_id=expense_id_to_remove)

    assert expenses_list == expected

def test_remove_raises_for_an_unknown_id(expenses_list):
    expense_id_to_remove = 99

    with pytest.raises(ValueError, match="#99"):
        remove(expenses_list, expense_id=expense_id_to_remove)

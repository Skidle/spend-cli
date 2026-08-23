import copy
from typing import Any

import pytest

from spend.commands import summary


@pytest.fixture
def expenses_list() -> list[dict[str, Any]]:
    return [
        {"id": 1, "amount": 30, "category": "food", "date": "2026-08-20"},
        {"id": 3, "amount": 60, "category": "transport", "date": "2026-08-20"},
        {"id": 2, "amount": 10, "category": "food", "date": "2026-08-15"},
    ]

def test_summary_totals_amounts_per_category(expenses_list: list[dict[str, Any]]) -> None:
    result = summary(expenses_list)

    assert result["rows"][0]["total"] == 60
    assert result["rows"][1]["total"] == 40

def test_summary_rows_are_sorted_by_total_descending(expenses_list: list[dict[str, Any]]) -> None:
    result = summary(expenses_list)

    assert result["rows"][0]["category"] == "transport"
    assert result["rows"][1]["category"] == "food"

def test_summary_calculates_fractions(expenses_list: list[dict[str, Any]]) -> None:
    result = summary(expenses_list)

    assert result["rows"][0]["fraction"] == 0.6
    assert result["rows"][1]["fraction"] == 0.4

def test_summary_filters_by_since_before_totalling(expenses_list: list[dict[str, Any]]) -> None:
    result = summary(expenses_list, since="2026-08-20")

    assert len(result["rows"]) == 2
    assert result["rows"][0]["fraction"] == pytest.approx(60 / 90)
    assert result["rows"][1]["fraction"] == pytest.approx(30 / 90)

def test_summary_returns_empty_rows_and_zero_total_for_no_expenses() -> None:
    expected: dict[str, Any] = {
        "rows": [],
        "grand_total": 0,
    }

    result = summary([], since="2026-08-20")

    assert result == expected

def test_summary_does_not_mutate_the_input(expenses_list: list[dict[str, Any]]) -> None:
    expenses = copy.deepcopy(expenses_list)

    summary(expenses_list)
    assert expenses == expenses_list

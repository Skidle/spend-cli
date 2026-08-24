import datetime
from dataclasses import dataclass

from spend.models import Expense, Ledger


def add(
    data: Ledger,
    amount: float,
    category: str,
    note: str | None = None,
    date: str | None = None
) -> Expense:
    if amount <= 0:
        raise ValueError(f"Amount {amount} should be positive.")
    
    if date is None:
        date = datetime.datetime.now(tz=datetime.UTC).date().isoformat()
    else:
        try:
            date = datetime.date.fromisoformat(date).isoformat()
        except ValueError as err:
            raise ValueError(f"Date {date} is not a valid ISO date (YYYY-MM-DD).") from err

    new_expense = Expense(
        id=data.next_id,
        amount=amount,
        category=category,
        date=date,
        note=note,
    )

    data.next_id += 1
    data.expenses.append(new_expense)

    return new_expense

def _filter_since(expenses: list[Expense], since: str | None) -> list[Expense]:
    if since is not None:
        return [e for e in expenses if e.date >= since]
    return expenses

def list_expenses(
    expenses: list[Expense],
    category: str | None = None,
    since: str | None = None
) -> list[Expense]:
    filtered = _filter_since(expenses, since)

    if category is not None:
        filtered = [e for e in filtered if e.category == category]

    return sorted(filtered, key=lambda e: (e.date, e.id))

@dataclass(frozen=True)
class SummaryRow:
    category: str
    total: float
    fraction: float

@dataclass(frozen=True)
class Summary:
    rows: list[SummaryRow]
    grand_total: float

def summary(expenses: list[Expense], since: str | None = None) -> Summary:
    filtered = _filter_since(expenses, since)

    totals: dict[str, float] = {}

    for e in filtered:
        category = e.category
        totals[category] = totals.get(category, 0) + e.amount

    grand_total = sum(totals.values())

    # comprehension over empty dict in totals produces [], no ZeroDivisionError
    unsorted_rows = [
        SummaryRow(
            category=category,
            total=total,
            fraction=total / grand_total,
        )
        for category, total in totals.items()
    ]

    rows = sorted(unsorted_rows, key=lambda r: r.total, reverse=True)

    return Summary(rows=rows, grand_total=grand_total)

def remove(expenses: list[Expense], expense_id: int) -> Expense:
    expense_to_remove = next((e for e in expenses if e.id == expense_id), None)

    if expense_to_remove is None:
        raise ValueError(f"Expense #{expense_id} not found.")

    expenses.remove(expense_to_remove)

    return expense_to_remove

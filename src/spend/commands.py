import datetime

def add(
    data: dict,
    amount: float,
    category: str,
    note: str | None = None,
    date: str | None = None
) -> dict:
    if date is None:
        date = datetime.date.today().isoformat()

    new_expense = {
        "id": data["next_id"],
        "amount": amount,
        "category": category,
        "date": date,
        "note": note,
    }

    data["next_id"] += 1
    data["expenses"].append(new_expense)

    return new_expense

def _filter_since(expenses: list[dict], since: str | None) -> list[dict]:
    if since is not None:
        return [e for e in expenses if e["date"] >= since]
    return expenses

def list_expenses(
    expenses: list[dict],
    category: str | None = None,
    since: str | None = None
) -> list[dict]:
    filtered = _filter_since(expenses, since)

    if category is not None:
        filtered = [e for e in filtered if e["category"] == category]

    return sorted(filtered, key=lambda e: (e["date"], e["id"]))

def summary(expenses: list[dict], since: str | None = None) -> dict:
    filtered = _filter_since(expenses, since)

    totals: dict[str, float] = {}

    for e in filtered:
        category = e["category"]
        totals[category] = totals.get(category, 0) + e["amount"]

    grand_total = sum(totals.values())

    # comprehension over empty dict produces [], no ZeroDivisionError
    unsorted_rows = [
        {
            "category": category,
            "total": total,
            "fraction": total / grand_total,
        }
        for category, total in totals.items()
    ]

    rows = sorted(unsorted_rows, key=lambda r: r["total"], reverse=True)

    return {"rows": rows, "grand_total": grand_total}

def remove(expenses: list[dict], expense_id: int) -> dict:
    expense_to_remove = next((e for e in expenses if e["id"] == expense_id), None)

    if expense_to_remove is None:
        raise ValueError(f"Expense #{expense_id} not found.")

    expenses.remove(expense_to_remove)

    return expense_to_remove

import datetime

def add(
    expenses: list[dict],
    amount: float,
    category: str,
    note: str | None = None,
    date: str | None = None
) -> dict:
    if date is None:
        date = datetime.date.today().isoformat()

    new_id = max([x["id"] for x in expenses], default=0) + 1

    new_expense = {
        "id": new_id,
        "amount": amount,
        "category": category,
        "date": date,
        "note": note,
    }

    expenses.append(new_expense)
    return new_expense

def list_expenses(
    expenses: list[dict],
    category: str | None = None,
    since: str | None = None
) -> list[dict]:
    items = expenses
    if category is not None:
        items = [e for e in items if e["category"] == category]
    if since is not None:
        items = [e for e in items if e["date"] >= since]

    return sorted(items, key=lambda e: (e["date"], e["id"]))

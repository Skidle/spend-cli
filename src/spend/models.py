from dataclasses import dataclass, field
from typing import TypedDict


class ExpenseDict(TypedDict):
    id: int
    amount: float
    category: str
    date: str
    note: str | None

@dataclass(frozen=True)
class Expense:
    id: int
    amount: float
    category: str
    date: str
    note: str | None = None

    def to_dict(self) -> ExpenseDict:
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
            "note": self.note,
        }

    @classmethod
    def from_dict(cls, d: ExpenseDict) -> Expense:
        return cls(
            id=d["id"],
            amount=d["amount"],
            category=d["category"],
            date=d["date"],
            note=d["note"]
        )

@dataclass
class Ledger:
    next_id: int = 1
    expenses: list[Expense] = field(default_factory=list[Expense])

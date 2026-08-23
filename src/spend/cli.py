import argparse
from pathlib import Path

from spend.store import load, save
from spend.commands import add

STORE_PATH = Path.home() / ".spend.json"

def main() -> None:
    parser = argparse.ArgumentParser(prog="spend", description="A command-line expense tracker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_add = subparsers.add_parser("add", help="add an expense")
    parser_add.add_argument("amount", type=float)
    parser_add.add_argument("category", type=str)
    parser_add.add_argument("--date", type=str)
    parser_add.add_argument("--note")

    parser_list = subparsers.add_parser("list", help="list expenses")
    parser_list.add_argument("--category", type=str)
    parser_list.add_argument("--since", type=str)

    parser_remove = subparsers.add_parser("remove", help="remove an expense")
    parser_remove.add_argument("id", type=int)

    parser_summary = subparsers.add_parser("summary", help="show totals")
    parser_summary.add_argument("--since", type=str)

    args = parser.parse_args()

    if args.command == "add":
        expenses = load(STORE_PATH)
        expense = add(expenses=expenses, amount=args.amount, category=args.category, note=args.note, date=args.date)
        save(STORE_PATH, expenses=expenses)
        print(f"added #{expense["id"]}  {expense["amount"]:.2f} {expense["category"]}   {expense["date"]}")
        
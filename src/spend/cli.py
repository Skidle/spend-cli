import argparse
import sys
from pathlib import Path
from typing import Any

from spend.commands import add, list_expenses, remove, summary
from spend.store import load, save

STORE_PATH = Path.home() / ".spend.json"

EMPTY_MESSAGE = "No expenses in that period."

def _format_row(expense: dict[str, Any]) -> str:
    return (
        f"#{expense['id']:<4} "
        f"{expense['date']:<12} "
        f"{expense['category']:<16} "
        f"{expense['amount']:>8.2f} "
        f"{expense['note'] or ''}"
    )

CATEGORY_W = 17
TOTAL_W = 9
FRACTION_W = 6
SUMMARY_W = CATEGORY_W + TOTAL_W + FRACTION_W

def _format_summary_row(row: dict[str, Any]) -> str:
    return (
        f"{row['category']:<{CATEGORY_W}}"
        f"{row['total']:>{TOTAL_W}.2f}"
        f"{row['fraction']:>{FRACTION_W}.0%}"
    )

def _build_parser() -> argparse.ArgumentParser:
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

    return parser

def _run(args: argparse.Namespace) -> None:
    data = load(STORE_PATH)

    if args.command == "add":
        expense = add(
            data,
            amount=args.amount,
            category=args.category,
            note=args.note,
            date=args.date
        )
        save(STORE_PATH, data)

        print(f"added {_format_row(expense)}")

    elif args.command == "list":
        expenses = list_expenses(data["expenses"], category=args.category, since=args.since)

        if not expenses:
            print(EMPTY_MESSAGE)
        else:
            for e in expenses:
                print(_format_row(e))

    elif args.command == "summary":
        result = summary(data["expenses"], since=args.since)

        if not result["rows"]:
            print(EMPTY_MESSAGE)
        else:
            for row in result["rows"]:
                print(_format_summary_row(row))
            print("-" * SUMMARY_W)
            print(f"{'total':<{CATEGORY_W}}{result['grand_total']:>{TOTAL_W}.2f}")

    elif args.command == "remove":
        removed_expense = remove(data.expenses, expense_id=args.id)

        save(STORE_PATH, data)

        print(f"removed {_format_row(removed_expense)}")

def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    try:
        _run(args)
    except ValueError as err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)

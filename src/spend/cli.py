import argparse

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
    print(args)

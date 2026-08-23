# spend-cli

A small command-line expense tracker. Expenses are stored locally in `~/.spend.json`.

Requires Python 3.14+ and [uv](https://docs.astral.sh/uv/).

## Install

```bash
uv sync
uv run spend --help
```

## Usage

Add an expense:

```bash
uv run spend add 15 transport --note="taxi"
uv run spend add 24.50 groceries --date=2026-08-19 --note="steak"
```

List expenses:

```bash
uv run spend list
uv run spend list --category=groceries
uv run spend list --since=2026-08-20
uv run spend list --category=groceries --since=2026-08-20
```

Show a summary:

```bash
uv run spend summary
uv run spend summary --since=2026-08-20
```

Remove an expense:

```bash
uv run spend remove 3
```

For all options:

```bash
uv run spend --help
uv run spend <command> --help
```

## Example

```bash
uv run spend summary --since=2026-08-20
```
```text
transport           105.00   89%
groceries            12.50   11%
--------------------------------
total               117.50
```

## Development

```bash
uv run pytest
uv run ruff check .
uv run mypy .
```

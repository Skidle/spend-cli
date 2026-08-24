import json
from pathlib import Path

from spend.models import Ledger, LedgerDict


def load(path: Path) -> Ledger:
    try:
        string = path.read_text(encoding="utf-8")
        data: LedgerDict = json.loads(string)
        return Ledger.from_dict(data)
    except FileNotFoundError:
        return Ledger()
    except json.JSONDecodeError as err:
        raise ValueError(f"The store at {path} is corrupt.") from err

def save(path: Path, data: Ledger) -> None:
    dict_data = data.to_dict()
    string = json.dumps(dict_data, indent=2)
    path.write_text(string, encoding="utf-8")

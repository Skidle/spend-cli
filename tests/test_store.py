from spend.store import load, save

def test_load_returns_what_save_wrote(tmp_path):
    expenses = [
        {"id": 1, "amount": 3, "category": "food"},
        {"id": 2, "amount": 10.5, "category": "transport"},
    ]

    path = tmp_path / "spend.json"
    save(path, expenses)

    result = load(path)
    assert result == expenses

def test_load_returns_empty_list_when_file_missing(tmp_path):
    path = tmp_path / "spend.json"
    result = load(path)
    assert result == []

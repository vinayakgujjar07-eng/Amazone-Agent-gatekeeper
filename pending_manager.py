"""
pending_manager.py
==================
Keeps the list of requests that are waiting for the customer to Confirm or Reject
(data/pending_requests.json). Saved in a file so it is not lost if the page refreshes.
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"
PENDING_FILE = DATA_DIR / "pending_requests.json"


def _path(path):
    return Path(path) if path else PENDING_FILE


def load_pending(path=None):
    """Return a list of pending items: {"request_id": ..., "request": {...}}"""
    file_path = _path(path)
    if not file_path.exists():
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def _save(items, path=None):
    file_path = _path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)


def add_pending(request_id, request, path=None):
    items = load_pending(path)
    items.append({"request_id": request_id, "request": request})
    _save(items, path)


def remove_pending(request_id, path=None):
    items = [i for i in load_pending(path) if i["request_id"] != request_id]
    _save(items, path)


def clear_pending(path=None):
    _save([], path)

"""
audit_logger.py
===============
Rule 8: EVERY request is recorded in the audit log (data/audit_log.csv).

Customer confirmation status values:
    Not required  - no confirmation was needed
    Pending       - waiting for the customer to Confirm or Reject
    Confirmed     - customer confirmed
    Rejected      - customer rejected

A request that needed confirmation appears TWICE in the log:
    1st row: ASK CUSTOMER  (Pending)
    2nd row: ALLOW or BLOCK (Confirmed / Rejected)
Both rows share the same Request ID, so the history is never overwritten.
"""

import csv
import uuid
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent / "data"
LOG_FILE = DATA_DIR / "audit_log.csv"

COLUMNS = [
    "Request ID",
    "Date and Time",
    "Agent ID",
    "Customer",
    "Requested Action",
    "Product Name",
    "Amount (INR)",
    "Decision",
    "Reason",
    "Rule Number",
    "Customer Confirmation Status",
    "Requested By",
]


def _path(path):
    return Path(path) if path else LOG_FILE


def _create_empty_log(file_path):
    file_path.parent.mkdir(parents=True, exist_ok=True)
    # utf-8-sig so Excel shows the rupee sign correctly
    with open(file_path, "w", newline="", encoding="utf-8-sig") as f:
        csv.writer(f).writerow(COLUMNS)


def reset_log(path=None):
    """Empty the log (keeps only the header row)."""
    _create_empty_log(_path(path))


def new_request_id():
    return "REQ-" + uuid.uuid4().hex[:8].upper()


def log_event(request_id, timestamp, agent_id, customer, action, product, amount,
              decision, reason, rule, confirmation_status="Not required",
              requested_by="AI Agent", path=None):
    """Add ONE row to the audit log."""
    file_path = _path(path)
    if not file_path.exists():
        _create_empty_log(file_path)

    row = [
        request_id, timestamp, agent_id, customer, action, product,
        "{:.2f}".format(float(amount or 0)), decision, reason, rule,
        confirmation_status, requested_by,
    ]
    with open(file_path, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(row)


def read_log(path=None):
    """Read the whole log as a pandas DataFrame (empty table if there is nothing yet)."""
    file_path = _path(path)
    if not file_path.exists():
        _create_empty_log(file_path)
    try:
        df = pd.read_csv(file_path, encoding="utf-8-sig")
    except (pd.errors.EmptyDataError, UnicodeDecodeError):
        _create_empty_log(file_path)
        df = pd.read_csv(file_path, encoding="utf-8-sig")
    for column in COLUMNS:
        if column not in df.columns:
            df[column] = ""
    return df[COLUMNS]


def request_summary(df):
    """
    Count requests made by AI agents (customer admin actions in the app are not counted).

    Each request is counted ONCE, using its LAST decision:
        allowed  - final decision is ALLOW
        blocked  - final decision is BLOCK
        pending  - final decision is still ASK CUSTOMER (waiting for the customer)
    'needed_confirmation' counts every request that was ever sent to the customer.
    """
    agent_rows = df[df["Requested By"] == "AI Agent"]
    if agent_rows.empty:
        return {"total": 0, "allowed": 0, "blocked": 0, "pending": 0, "needed_confirmation": 0}

    final = agent_rows.groupby("Request ID", sort=False).tail(1)
    needed = agent_rows[agent_rows["Decision"] == "ASK CUSTOMER"]["Request ID"].nunique()
    return {
        "total": int(len(final)),
        "allowed": int((final["Decision"] == "ALLOW").sum()),
        "blocked": int((final["Decision"] == "BLOCK").sum()),
        "pending": int((final["Decision"] == "ASK CUSTOMER").sum()),
        "needed_confirmation": int(needed),
    }


def log_as_csv_bytes(df):
    """The log as CSV bytes for the Download button."""
    return df.to_csv(index=False).encode("utf-8-sig")

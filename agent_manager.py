"""
agent_manager.py
================
Keeps the list of AI agents in a simple JSON file (data/agents.json).

Each agent record looks like this:
    {
        "agent_id": "AGT-001",
        "customer_name": "Rahul Verma",
        "permission_level": "Full shopping",     # or "Read-only"
        "status": "Active",                      # or "Revoked"
        "registered_at": "2026-11-20 10:30:00",
        "revoked_at": ""                         # filled when revoked
    }
"""

import json
from datetime import datetime
from pathlib import Path

from decision_engine import (
    PERMISSIONS,
    STATUS_ACTIVE,
    STATUS_REVOKED,
)

DATA_DIR = Path(__file__).resolve().parent / "data"
AGENTS_FILE = DATA_DIR / "agents.json"

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# Simulated demo agents (fictional people, no real data)
DEFAULT_AGENTS = [
    {
        "agent_id": "AGT-001",
        "customer_name": "Rahul Verma",
        "permission_level": "Full shopping",
        "status": "Active",
        "registered_at": "2026-11-01 09:00:00",
        "revoked_at": "",
    },
    {
        "agent_id": "AGT-002",
        "customer_name": "Rahul Verma",
        "permission_level": "Full shopping",
        "status": "Revoked",
        "registered_at": "2026-11-01 09:05:00",
        "revoked_at": "2026-11-10 18:30:00",
    },
    {
        "agent_id": "AGT-003",
        "customer_name": "Priya Sharma",
        "permission_level": "Read-only",
        "status": "Active",
        "registered_at": "2026-11-02 11:15:00",
        "revoked_at": "",
    },
]


def _now():
    return datetime.now().strftime(TIME_FORMAT)


def _path(path):
    return Path(path) if path else AGENTS_FILE


def save_agents(agents, path=None):
    """Save the agents dictionary {agent_id: record} to the JSON file."""
    file_path = _path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(list(agents.values()), f, indent=2, ensure_ascii=False)


def reset_agents(path=None):
    """Put the three demo agents back (used by the 'Reset demo data' button)."""
    agents = {a["agent_id"]: dict(a) for a in DEFAULT_AGENTS}
    save_agents(agents, path)
    return agents


def load_agents(path=None):
    """Load agents as a dictionary {agent_id: record}. Creates demo data if file is missing."""
    file_path = _path(path)
    if not file_path.exists():
        return reset_agents(path)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            records = json.load(f)
    except (json.JSONDecodeError, OSError):
        return reset_agents(path)
    return {r["agent_id"]: r for r in records}


def next_agent_id(agents):
    """Create the next ID: AGT-001, AGT-002, ..."""
    numbers = []
    for agent_id in agents:
        if agent_id.startswith("AGT-") and agent_id[4:].isdigit():
            numbers.append(int(agent_id[4:]))
    next_number = (max(numbers) + 1) if numbers else 1
    return "AGT-{:03d}".format(next_number)


def register_agent(customer_name, permission_level, status=STATUS_ACTIVE, agent_id=None, path=None):
    """Register a new agent. Raises ValueError with a friendly message if input is wrong."""
    agents = load_agents(path)

    customer_name = (customer_name or "").strip()
    if not customer_name:
        raise ValueError("Please enter the customer name.")
    if permission_level not in PERMISSIONS:
        raise ValueError("Permission level must be one of: " + ", ".join(PERMISSIONS))
    if status not in (STATUS_ACTIVE, STATUS_REVOKED):
        raise ValueError("Status must be Active or Revoked.")

    agent_id = (agent_id or "").strip().upper() or next_agent_id(agents)
    if agent_id in agents:
        raise ValueError("Agent ID {} already exists.".format(agent_id))

    now = _now()
    record = {
        "agent_id": agent_id,
        "customer_name": customer_name,
        "permission_level": permission_level,
        "status": status,
        "registered_at": now,
        "revoked_at": now if status == STATUS_REVOKED else "",
    }
    agents[agent_id] = record
    save_agents(agents, path)
    return record


def revoke_agent(agent_id, path=None):
    """Revoke an agent and record the date and time. Raises ValueError if not possible."""
    agents = load_agents(path)
    if agent_id not in agents:
        raise ValueError("Agent {} was not found.".format(agent_id))
    if agents[agent_id]["status"] == STATUS_REVOKED:
        raise ValueError("Agent {} is already revoked.".format(agent_id))

    agents[agent_id]["status"] = STATUS_REVOKED
    agents[agent_id]["revoked_at"] = _now()
    save_agents(agents, path)
    return agents[agent_id]


def count_agents(agents):
    """Return (total, active, revoked)."""
    total = len(agents)
    active = sum(1 for a in agents.values() if a["status"] == STATUS_ACTIVE)
    revoked = sum(1 for a in agents.values() if a["status"] == STATUS_REVOKED)
    return total, active, revoked

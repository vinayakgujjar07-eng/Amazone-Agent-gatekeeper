"""
decision_engine.py
==================
The "brain" of Agent Gatekeeper.

It receives ONE request from an AI agent and returns ONE decision:
    ALLOW          - the action is permitted
    ASK CUSTOMER   - the customer must confirm first
    BLOCK          - the action is prohibited

The rules are checked in a fixed PRIORITY ORDER (Rule 1 first).
The engine stops at the first rule that applies. Because "unknown agent"
and "revoked agent" are checked first, a bad agent can never reach the
rules that would ALLOW something.

This is an independent academic prototype. It is NOT connected to Amazon
or any real customer account.
"""

# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------
SPENDING_LIMIT = 5000  # Rs. 5,000 - money actions ABOVE this need customer OK

# ---------------------------------------------------------------------------
# The nine business activities
# ---------------------------------------------------------------------------
READ_ONLY_ACTIONS = (
    "View product details",
    "View product prices",
    "View order history",
)

MONEY_ACTIONS = (
    "Place an order",
    "Cancel an order",
    "Request a return",
    "Request a refund",
)

# Register / Revoke are done by the CUSTOMER in the app, never by an AI agent.
MANAGEMENT_ACTIONS = (
    "Register an AI agent",
    "Revoke an AI agent",
)

ALL_ACTIONS = READ_ONLY_ACTIONS + MONEY_ACTIONS + MANAGEMENT_ACTIONS

# ---------------------------------------------------------------------------
# What each permission level lets an agent do (used by Rule 3)
# ---------------------------------------------------------------------------
PERMISSION_READ_ONLY = "Read-only"
PERMISSION_FULL = "Full shopping"

PERMISSIONS = {
    PERMISSION_READ_ONLY: READ_ONLY_ACTIONS,
    PERMISSION_FULL: READ_ONLY_ACTIONS + MONEY_ACTIONS,
}

STATUS_ACTIVE = "Active"
STATUS_REVOKED = "Revoked"

DECISION_ALLOW = "ALLOW"
DECISION_ASK = "ASK CUSTOMER"
DECISION_BLOCK = "BLOCK"

# ---------------------------------------------------------------------------
# The eight security rules (title + simple explanation, used in the app/report)
# ---------------------------------------------------------------------------
RULES = {
    1: {
        "title": "Unknown agent",
        "decision": "BLOCK",
        "explanation": "If the agent ID is not in the registered list, every request is blocked.",
    },
    2: {
        "title": "Revoked agent",
        "decision": "BLOCK",
        "explanation": "If the customer has revoked the agent, every request is blocked. "
                       "This is checked early so a revoked agent cannot bypass anything.",
    },
    3: {
        "title": "Out-of-scope or suspicious action",
        "decision": "BLOCK",
        "explanation": "An agent may only do what its permission level allows, for its own "
                       "customer, with a valid amount. Anything else is blocked.",
    },
    4: {
        "title": "Read-only action",
        "decision": "ALLOW",
        "explanation": "A registered, active agent may view product details, prices and "
                       "order history.",
    },
    5: {
        "title": "Money action within the limit",
        "decision": "ALLOW",
        "explanation": "Place order, cancel, return or refund up to the spending limit "
                       "(Rs. 5,000) is allowed.",
    },
    6: {
        "title": "Money action above the limit",
        "decision": "ASK CUSTOMER",
        "explanation": "Above the spending limit, the request waits until the customer "
                       "confirms.",
    },
    7: {
        "title": "Customer confirmation recorded",
        "decision": "ALLOW / BLOCK",
        "explanation": "An above-limit action is allowed only after the customer's "
                       "confirmation is recorded. If the customer rejects, it is blocked.",
    },
    8: {
        "title": "Audit log",
        "decision": "Applies to all",
        "explanation": "Every request, whatever the decision, is written to the audit log.",
    },
}


# ---------------------------------------------------------------------------
# Small helper functions
# ---------------------------------------------------------------------------
def format_inr(amount):
    """Show an amount in Indian Rupees with the rupee sign, e.g. 10000 -> 10,000 with the sign in front."""
    return "\u20b9{:,.0f}".format(amount)


def is_money_action(action):
    return action in MONEY_ACTIONS


def is_read_only_action(action):
    return action in READ_ONLY_ACTIONS


def _to_amount(value):
    """Convert the amount to a number. Returns None if it is not a valid number."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _result(decision, rule, reason, amount, agent_status):
    """Build the answer dictionary that the app and the tests use."""
    return {
        "decision": decision,
        "rule": rule,
        "rule_title": RULES[rule]["title"],
        "reason": reason,
        "amount": amount,
        "agent_status": agent_status,
    }


# ---------------------------------------------------------------------------
# THE DECISION ENGINE
# ---------------------------------------------------------------------------
def evaluate_request(request, agents, confirmation=None, limit=SPENDING_LIMIT):
    """
    Evaluate one request from an AI agent.

    request      : dict with keys agent_id, customer, action, product, amount
    agents       : dict {agent_id: agent_record} of registered agents
    confirmation : None (first time), or "Confirmed" / "Rejected" (customer's answer
                   to an ASK CUSTOMER request)
    limit        : spending limit in rupees

    Returns a dict: decision, rule, rule_title, reason, amount, agent_status
    """
    agent_id = str(request.get("agent_id", "")).strip()
    customer = str(request.get("customer", "")).strip()
    action = str(request.get("action", "")).strip()
    raw_amount = _to_amount(request.get("amount", 0))
    amount = raw_amount if raw_amount is not None else 0.0

    agent = agents.get(agent_id)

    # ---- RULE 1: unknown agent -> BLOCK -----------------------------------
    if agent is None:
        return _result(
            DECISION_BLOCK, 1,
            "Agent ID '{}' is not registered. Unknown agents are always blocked.".format(agent_id),
            amount, "Unknown",
        )

    status = agent.get("status", "")

    # ---- RULE 2: revoked (or not active) agent -> BLOCK -------------------
    if status != STATUS_ACTIVE:
        return _result(
            DECISION_BLOCK, 2,
            "Agent {} is {}. Revoked agents are always blocked.".format(agent_id, status.lower() or "not active"),
            amount, status or "Not active",
        )

    # ---- RULE 3: out-of-scope or suspicious action -> BLOCK ---------------
    if action not in ALL_ACTIONS:
        return _result(
            DECISION_BLOCK, 3,
            "'{}' is not a recognised shopping action.".format(action),
            amount, status,
        )

    if action in MANAGEMENT_ACTIONS:
        return _result(
            DECISION_BLOCK, 3,
            "AI agents cannot '{}'. Only the customer can do this inside the app.".format(action.lower()),
            amount, status,
        )

    permitted = PERMISSIONS.get(agent.get("permission_level"), ())
    if action not in permitted:
        return _result(
            DECISION_BLOCK, 3,
            "Agent {} has '{}' permission, which does not allow '{}'.".format(
                agent_id, agent.get("permission_level"), action.lower()),
            amount, status,
        )

    if customer.lower() != str(agent.get("customer_name", "")).strip().lower():
        return _result(
            DECISION_BLOCK, 3,
            "Suspicious request: agent {} belongs to '{}', but the request is for '{}'.".format(
                agent_id, agent.get("customer_name"), customer or "(no customer)"),
            amount, status,
        )

    if is_money_action(action) and (raw_amount is None or raw_amount <= 0):
        return _result(
            DECISION_BLOCK, 3,
            "Suspicious request: '{}' needs a valid amount greater than zero.".format(action.lower()),
            amount, status,
        )

    # ---- RULE 4: read-only action -> ALLOW --------------------------------
    if is_read_only_action(action):
        return _result(
            DECISION_ALLOW, 4,
            "Read-only action by a registered, active agent. No money is involved.",
            amount, status,
        )

    # ---- From here the action is a MONEY action ---------------------------
    # ---- RULE 5: within the limit -> ALLOW --------------------------------
    if amount <= limit:
        return _result(
            DECISION_ALLOW, 5,
            "{} is within the {} spending limit.".format(format_inr(amount), format_inr(limit)),
            amount, status,
        )

    # ---- RULE 7: the customer has answered an ASK CUSTOMER request --------
    if confirmation == "Confirmed":
        return _result(
            DECISION_ALLOW, 7,
            "Customer confirmation recorded for {} (above the {} limit). Action authorised.".format(
                format_inr(amount), format_inr(limit)),
            amount, status,
        )
    if confirmation == "Rejected":
        return _result(
            DECISION_BLOCK, 7,
            "Customer rejected this {} request. Action not authorised.".format(format_inr(amount)),
            amount, status,
        )

    # ---- RULE 6: above the limit, no confirmation yet -> ASK CUSTOMER -----
    return _result(
        DECISION_ASK, 6,
        "{} is above the {} spending limit. Customer confirmation is required.".format(
            format_inr(amount), format_inr(limit)),
        amount, status,
    )

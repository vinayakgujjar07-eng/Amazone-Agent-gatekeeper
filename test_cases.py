"""
test_cases.py
=============
The SIX required test cases from the assignment.

run_six_cases() sends each input to the REAL decision engine and compares the
actual answer with the expected answer. Nothing is hard-coded as "passed".

It uses its own small set of test agents, so it never touches the real data files.
"""

from decision_engine import evaluate_request

# Test agents (independent of data/agents.json)
TEST_AGENTS = {
    "AGT-001": {
        "agent_id": "AGT-001", "customer_name": "Rahul Verma",
        "permission_level": "Full shopping", "status": "Active",
    },
    "AGT-002": {
        "agent_id": "AGT-002", "customer_name": "Rahul Verma",
        "permission_level": "Full shopping", "status": "Revoked",
    },
    "AGT-003": {
        "agent_id": "AGT-003", "customer_name": "Priya Sharma",
        "permission_level": "Read-only", "status": "Active",
    },
}

SIX_CASES = [
    {
        "no": 1,
        "scenario": "Registered agent checks product prices",
        "request": {"agent_id": "AGT-001", "customer": "Rahul Verma",
                    "action": "View product prices", "product": "Wireless Earbuds", "amount": 0},
        "expected": "ALLOW", "expected_rule": 4,
    },
    {
        "no": 2,
        "scenario": "Unknown agent tries to place an order",
        "request": {"agent_id": "AGT-999", "customer": "Rahul Verma",
                    "action": "Place an order", "product": "Wireless Earbuds", "amount": 2000},
        "expected": "BLOCK", "expected_rule": 1,
    },
    {
        "no": 3,
        "scenario": "Registered agent tries to buy a Rs. 10,000 product (limit Rs. 5,000)",
        "request": {"agent_id": "AGT-001", "customer": "Rahul Verma",
                    "action": "Place an order", "product": "Smartphone", "amount": 10000},
        "expected": "ASK CUSTOMER", "expected_rule": 6,
    },
    {
        "no": 4,
        "scenario": "Registered agent tries to buy a Rs. 2,000 product",
        "request": {"agent_id": "AGT-001", "customer": "Rahul Verma",
                    "action": "Place an order", "product": "Wireless Earbuds", "amount": 2000},
        "expected": "ALLOW", "expected_rule": 5,
    },
    {
        "no": 5,
        "scenario": "Revoked agent tries to place an order",
        "request": {"agent_id": "AGT-002", "customer": "Rahul Verma",
                    "action": "Place an order", "product": "Wireless Earbuds", "amount": 2000},
        "expected": "BLOCK", "expected_rule": 2,
    },
    {
        "no": 6,
        "scenario": "Registered agent requests a Rs. 8,000 refund",
        "request": {"agent_id": "AGT-001", "customer": "Rahul Verma",
                    "action": "Request a refund", "product": "Smart Watch", "amount": 8000},
        "expected": "ASK CUSTOMER", "expected_rule": 6,
    },
]


def run_six_cases():
    """Run all six cases. Returns a list of result rows (dictionaries)."""
    rows = []
    for case in SIX_CASES:
        result = evaluate_request(case["request"], TEST_AGENTS)
        passed = (result["decision"] == case["expected"]
                  and result["rule"] == case["expected_rule"])
        req = case["request"]
        rows.append({
            "Test": case["no"],
            "Scenario": case["scenario"],
            "Input": "{} | {} | {} | Rs. {:,.0f}".format(
                req["agent_id"], req["action"], req["product"], float(req["amount"])),
            "Expected": "{} (Rule {})".format(case["expected"], case["expected_rule"]),
            "Actual": "{} (Rule {})".format(result["decision"], result["rule"]),
            "Result": "PASS" if passed else "FAIL",
            "Explanation": result["reason"],
        })
    return rows

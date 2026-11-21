"""
tests/test_gatekeeper.py
========================
Run from the AgentGate folder with:

    python tests/test_gatekeeper.py

Part 1 prints the SIX required test cases (and saves tests/test_results.csv).
Part 2 runs extra edge-case tests (limit boundary, confirmation, priority order,
audit log, agent registration/revocation) using temporary files, so your real
data files are never changed.
"""

import csv
import os
import sys
import tempfile
import unittest

# Make the project folder importable when running from anywhere
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import agent_manager as am            # noqa: E402
import audit_logger as al             # noqa: E402
from decision_engine import evaluate_request   # noqa: E402
from test_cases import TEST_AGENTS, run_six_cases   # noqa: E402


def make_request(agent_id="AGT-001", customer="Rahul Verma", action="Place an order",
                 product="Test Product", amount=2000):
    return {"agent_id": agent_id, "customer": customer, "action": action,
            "product": product, "amount": amount}


# ---------------------------------------------------------------------------
# The SIX required test cases (each one is also a unittest)
# ---------------------------------------------------------------------------
class TestSixRequiredCases(unittest.TestCase):

    def test_1_registered_agent_checks_prices_allow(self):
        r = evaluate_request(make_request(action="View product prices", amount=0), TEST_AGENTS)
        self.assertEqual(r["decision"], "ALLOW")
        self.assertEqual(r["rule"], 4)

    def test_2_unknown_agent_places_order_block(self):
        r = evaluate_request(make_request(agent_id="AGT-999"), TEST_AGENTS)
        self.assertEqual(r["decision"], "BLOCK")
        self.assertEqual(r["rule"], 1)

    def test_3_purchase_10000_asks_customer(self):
        r = evaluate_request(make_request(amount=10000), TEST_AGENTS)
        self.assertEqual(r["decision"], "ASK CUSTOMER")
        self.assertEqual(r["rule"], 6)

    def test_4_purchase_2000_allow(self):
        r = evaluate_request(make_request(amount=2000), TEST_AGENTS)
        self.assertEqual(r["decision"], "ALLOW")
        self.assertEqual(r["rule"], 5)

    def test_5_revoked_agent_places_order_block(self):
        r = evaluate_request(make_request(agent_id="AGT-002"), TEST_AGENTS)
        self.assertEqual(r["decision"], "BLOCK")
        self.assertEqual(r["rule"], 2)

    def test_6_refund_8000_asks_customer(self):
        r = evaluate_request(make_request(action="Request a refund", amount=8000), TEST_AGENTS)
        self.assertEqual(r["decision"], "ASK CUSTOMER")
        self.assertEqual(r["rule"], 6)


# ---------------------------------------------------------------------------
# Extra edge-case tests
# ---------------------------------------------------------------------------
class TestExtraRules(unittest.TestCase):

    def test_exactly_5000_is_allowed(self):
        r = evaluate_request(make_request(amount=5000), TEST_AGENTS)
        self.assertEqual((r["decision"], r["rule"]), ("ALLOW", 5))

    def test_5001_asks_customer(self):
        r = evaluate_request(make_request(amount=5001), TEST_AGENTS)
        self.assertEqual((r["decision"], r["rule"]), ("ASK CUSTOMER", 6))

    def test_confirmed_above_limit_is_allowed_rule_7(self):
        r = evaluate_request(make_request(amount=10000), TEST_AGENTS, confirmation="Confirmed")
        self.assertEqual((r["decision"], r["rule"]), ("ALLOW", 7))

    def test_rejected_above_limit_is_blocked_rule_7(self):
        r = evaluate_request(make_request(amount=10000), TEST_AGENTS, confirmation="Rejected")
        self.assertEqual((r["decision"], r["rule"]), ("BLOCK", 7))

    def test_revoked_agent_cannot_use_confirmation(self):
        # Agent revoked while the request was waiting: confirmation must NOT help it.
        r = evaluate_request(make_request(agent_id="AGT-002", amount=10000),
                             TEST_AGENTS, confirmation="Confirmed")
        self.assertEqual((r["decision"], r["rule"]), ("BLOCK", 2))

    def test_revoked_beats_above_limit_priority(self):
        r = evaluate_request(make_request(agent_id="AGT-002", amount=10000), TEST_AGENTS)
        self.assertEqual((r["decision"], r["rule"]), ("BLOCK", 2))

    def test_unknown_agent_read_only_still_blocked(self):
        r = evaluate_request(make_request(agent_id="AGT-999", action="View order history", amount=0),
                             TEST_AGENTS)
        self.assertEqual((r["decision"], r["rule"]), ("BLOCK", 1))

    def test_read_only_agent_cannot_place_order(self):
        r = evaluate_request(make_request(agent_id="AGT-003", customer="Priya Sharma", amount=500),
                             TEST_AGENTS)
        self.assertEqual((r["decision"], r["rule"]), ("BLOCK", 3))

    def test_read_only_agent_can_view_order_history(self):
        r = evaluate_request(make_request(agent_id="AGT-003", customer="Priya Sharma",
                                          action="View order history", amount=0), TEST_AGENTS)
        self.assertEqual((r["decision"], r["rule"]), ("ALLOW", 4))

    def test_agent_for_wrong_customer_is_blocked(self):
        r = evaluate_request(make_request(customer="Someone Else"), TEST_AGENTS)
        self.assertEqual((r["decision"], r["rule"]), ("BLOCK", 3))

    def test_agent_cannot_revoke_agents(self):
        r = evaluate_request(make_request(action="Revoke an AI agent", amount=0), TEST_AGENTS)
        self.assertEqual((r["decision"], r["rule"]), ("BLOCK", 3))

    def test_agent_cannot_register_agents(self):
        r = evaluate_request(make_request(action="Register an AI agent", amount=0), TEST_AGENTS)
        self.assertEqual((r["decision"], r["rule"]), ("BLOCK", 3))

    def test_negative_amount_is_blocked(self):
        r = evaluate_request(make_request(amount=-500), TEST_AGENTS)
        self.assertEqual((r["decision"], r["rule"]), ("BLOCK", 3))

    def test_invalid_action_is_blocked(self):
        r = evaluate_request(make_request(action="Delete all orders"), TEST_AGENTS)
        self.assertEqual((r["decision"], r["rule"]), ("BLOCK", 3))

    def test_cancel_and_return_follow_the_limit(self):
        small = evaluate_request(make_request(action="Cancel an order", amount=1500), TEST_AGENTS)
        big = evaluate_request(make_request(action="Request a return", amount=9000), TEST_AGENTS)
        self.assertEqual(small["decision"], "ALLOW")
        self.assertEqual(big["decision"], "ASK CUSTOMER")


class TestFilesAndLog(unittest.TestCase):
    """Uses a temporary folder so the real data files are not touched."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.agents_path = os.path.join(self.tmp.name, "agents.json")
        self.log_path = os.path.join(self.tmp.name, "audit_log.csv")

    def tearDown(self):
        self.tmp.cleanup()

    def test_register_then_revoke_agent(self):
        record = am.register_agent("Test Customer", "Full shopping", path=self.agents_path)
        self.assertEqual(record["status"], "Active")
        revoked = am.revoke_agent(record["agent_id"], path=self.agents_path)
        self.assertEqual(revoked["status"], "Revoked")
        self.assertTrue(revoked["revoked_at"])
        # Revoked agent is blocked by the engine
        agents = am.load_agents(self.agents_path)
        r = evaluate_request(make_request(agent_id=record["agent_id"], customer="Test Customer"), agents)
        self.assertEqual((r["decision"], r["rule"]), ("BLOCK", 2))

    def test_duplicate_agent_id_is_rejected(self):
        am.register_agent("A", "Read-only", agent_id="AGT-050", path=self.agents_path)
        with self.assertRaises(ValueError):
            am.register_agent("B", "Read-only", agent_id="AGT-050", path=self.agents_path)

    def test_audit_log_records_every_request_and_summary(self):
        al.log_event("REQ-1", "2026-11-20 10:00:00", "AGT-001", "Rahul Verma", "Place an order",
                     "Smartphone", 10000, "ASK CUSTOMER", "Above limit", 6, "Pending",
                     path=self.log_path)
        al.log_event("REQ-1", "2026-11-20 10:01:00", "AGT-001", "Rahul Verma", "Place an order",
                     "Smartphone", 10000, "ALLOW", "Confirmed", 7, "Confirmed",
                     path=self.log_path)
        al.log_event("REQ-2", "2026-11-20 10:02:00", "AGT-999", "Rahul Verma", "Place an order",
                     "Earbuds", 2000, "BLOCK", "Unknown", 1, "Not required",
                     path=self.log_path)
        df = al.read_log(self.log_path)
        self.assertEqual(len(df), 3)
        summary = al.request_summary(df)
        self.assertEqual(summary["total"], 2)            # 2 requests (REQ-1 counted once)
        self.assertEqual(summary["allowed"], 1)
        self.assertEqual(summary["blocked"], 1)
        self.assertEqual(summary["pending"], 0)
        self.assertEqual(summary["needed_confirmation"], 1)


# ---------------------------------------------------------------------------
# Run everything and print a readable report
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")   # so the rupee sign prints on Windows
    except Exception:
        pass

    print("=" * 78)
    print("AGENT GATEKEEPER - SIX REQUIRED TEST CASES")
    print("=" * 78)
    rows = run_six_cases()
    for row in rows:
        print("TEST {}: {}".format(row["Test"], row["Scenario"]))
        print("   Input    : {}".format(row["Input"]))
        print("   Expected : {}".format(row["Expected"]))
        print("   Actual   : {}".format(row["Actual"]))
        print("   Result   : {}".format(row["Result"]))
        print("   Why      : {}".format(row["Explanation"]))
        print("-" * 78)

    passed = sum(1 for r in rows if r["Result"] == "PASS")
    print("SUMMARY: {} of {} required test cases passed.".format(passed, len(rows)))

    out_file = os.path.join(ROOT, "tests", "test_results.csv")
    with open(out_file, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print("Results saved to tests/test_results.csv")

    print("\nRunning the full automated test suite (required + extra tests)...\n")
    unittest.main(argv=["test_gatekeeper"], verbosity=2)

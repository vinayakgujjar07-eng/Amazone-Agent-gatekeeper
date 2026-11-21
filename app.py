"""
app.py  -  Agent Gatekeeper: Online Shopping Security System
============================================================
Run with:   streamlit run app.py

Independent academic prototype inspired by online shopping platforms.
NOT connected to Amazon or any real customer account. All data is simulated.
"""

from datetime import datetime

import pandas as pd
import streamlit as st

import agent_manager as am
import audit_logger as al
import pending_manager as pm
from decision_engine import (
    ALL_ACTIONS,
    DECISION_ALLOW,
    DECISION_ASK,
    DECISION_BLOCK,
    PERMISSIONS,
    READ_ONLY_ACTIONS,
    RULES,
    SPENDING_LIMIT,
    evaluate_request,
    format_inr,
)
from test_cases import run_six_cases

st.set_page_config(page_title="Agent Gatekeeper", page_icon="\U0001f6e1\ufe0f", layout="wide")

# Simulated product catalogue (fictional prices in rupees)
CATALOG = {
    "Wireless Earbuds": 2000,
    "Cotton T-Shirt": 800,
    "Book Set": 1200,
    "Running Shoes": 3500,
    "Mixer Grinder": 4500,
    "Smart Watch": 8000,
    "Smartphone": 10000,
    "Laptop": 45000,
}
OTHER_PRODUCT = "Other (type below)"

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


# ---------------------------------------------------------------------------
# Helper functions that connect the engine, the agent list, the log and the queue
# ---------------------------------------------------------------------------
def process_request(request):
    """Send one agent request through the Gatekeeper, log it, and queue it if needed."""
    agents = am.load_agents()
    request_id = al.new_request_id()
    result = evaluate_request(request, agents)

    if result["decision"] == DECISION_ASK:
        confirmation_status = "Pending"
        pm.add_pending(request_id, request)
    else:
        confirmation_status = "Not required"

    al.log_event(
        request_id, request["timestamp"], request["agent_id"], request["customer"],
        request["action"], request["product"], request["amount"], result["decision"],
        result["reason"], result["rule"], confirmation_status, requested_by="AI Agent",
    )
    return request_id, result


def process_confirmation(pending_item, choice):
    """The customer clicked Confirm or Reject. Re-check the rules, then log the outcome."""
    request = pending_item["request"]
    agents = am.load_agents()          # re-load: the agent may have been revoked meanwhile
    result = evaluate_request(request, agents, confirmation=choice)

    al.log_event(
        pending_item["request_id"], datetime.now().strftime(TIME_FORMAT), request["agent_id"],
        request["customer"], request["action"], request["product"], request["amount"],
        result["decision"], result["reason"], result["rule"], choice, requested_by="AI Agent",
    )
    pm.remove_pending(pending_item["request_id"])
    return result


def show_decision(result, request_id=None):
    """Display the decision card (Section E: Decision Engine)."""
    decision = result["decision"]
    if decision == DECISION_ALLOW:
        st.success("DECISION: ALLOW")
    elif decision == DECISION_ASK:
        st.warning("DECISION: ASK CUSTOMER")
    else:
        st.error("DECISION: BLOCK")

    col1, col2, col3 = st.columns(3)
    col1.metric("Rule responsible", "Rule {}".format(result["rule"]))
    col2.metric("Transaction amount", format_inr(result["amount"]))
    col3.metric("Agent authorization status", result["agent_status"])
    st.write("**Rule:** {}".format(result["rule_title"]))
    st.write("**Reason:** {}".format(result["reason"]))
    if request_id:
        st.caption("Request ID: {}".format(request_id))


# ---------------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------------
st.sidebar.title("\U0001f6e1\ufe0f Agent Gatekeeper")
page = st.sidebar.radio(
    "Go to section",
    [
        "A. Dashboard",
        "B. Agent Registration",
        "C. Agent Revocation",
        "D. Shopping Request Simulator",
        "F. Customer Confirmation",
        "G. Audit Log",
        "H. Security Summary",
        "Testing Results",
    ],
)
st.sidebar.info("Spending limit: **{}**\n\nAll data is simulated.".format(format_inr(SPENDING_LIMIT)))

with st.sidebar.expander("Reset demo data"):
    st.caption("Restores 3 demo agents and empties the audit log and pending list.")
    sure = st.checkbox("I understand this deletes the current log")
    if st.button("Reset now", disabled=not sure):
        am.reset_agents()
        al.reset_log()
        pm.clear_pending()
        st.session_state.pop("last_result", None)
        st.success("Demo data reset.")
        st.rerun()

st.title("Agent Gatekeeper \u2013 Online Shopping Security System")

# ---------------------------------------------------------------------------
# A. DASHBOARD
# ---------------------------------------------------------------------------
if page == "A. Dashboard":
    st.write(
        "Agent Gatekeeper is a security checkpoint between a customer's AI shopping agent and "
        "an online store. It checks every request and decides: **ALLOW**, **ASK CUSTOMER**, or **BLOCK**."
    )
    st.caption("Independent academic prototype inspired by online shopping platforms (reference: Amazon). "
               "Not connected to, approved by, or partnered with Amazon.")

    agents = am.load_agents()
    total_agents, active_agents, revoked_agents = am.count_agents(agents)
    summary = al.request_summary(al.read_log())

    st.subheader("Agents")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total registered agents", total_agents)
    c2.metric("Active agents", active_agents)
    c3.metric("Revoked agents", revoked_agents)

    st.subheader("Requests")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total requests processed", summary["total"])
    c2.metric("Allowed requests", summary["allowed"])
    c3.metric("Blocked requests", summary["blocked"])
    c4.metric("Requiring customer confirmation", summary["needed_confirmation"])
    st.caption("Each request is counted once, using its latest decision. "
               "Register/Revoke actions done by the customer are not counted as agent requests.")

    with st.expander("The 8 security rules (checked in this order)"):
        for number, rule in RULES.items():
            st.markdown("**Rule {} \u2013 {}** ({})  \n{}".format(
                number, rule["title"], rule["decision"], rule["explanation"]))

# ---------------------------------------------------------------------------
# B. AGENT REGISTRATION
# ---------------------------------------------------------------------------
elif page == "B. Agent Registration":
    st.header("Agent Registration")
    agents = am.load_agents()
    suggested_id = am.next_agent_id(agents)

    with st.form("register_form", clear_on_submit=False):
        customer_name = st.text_input("Customer name")
        agent_id = st.text_input("Agent ID", value=suggested_id,
                                 help="Auto-generated. You may type your own unique ID.")
        permission = st.selectbox("Permission level", list(PERMISSIONS.keys()), index=1,
                                  help="Read-only agents can only view. Full shopping agents can also place orders, cancel, return and refund.")
        status = st.selectbox("Agent status", ["Active", "Revoked"])
        submitted = st.form_submit_button("Register agent")

    if submitted:
        try:
            record = am.register_agent(customer_name, permission, status, agent_id)
            al.log_event(
                al.new_request_id(), datetime.now().strftime(TIME_FORMAT), record["agent_id"],
                record["customer_name"], "Register an AI agent", "-", 0, DECISION_ALLOW,
                "Customer registered the agent in the app ({}, {}).".format(
                    record["permission_level"], record["status"]),
                8, "Not required", requested_by="Customer (app)",
            )
            st.success("Agent {} registered for {}.".format(record["agent_id"], record["customer_name"]))
        except ValueError as error:
            st.error(str(error))

    st.subheader("Registered agents")
    agents = am.load_agents()
    st.dataframe(pd.DataFrame(list(agents.values())), width="stretch", hide_index=True)

# ---------------------------------------------------------------------------
# C. AGENT REVOCATION
# ---------------------------------------------------------------------------
elif page == "C. Agent Revocation":
    st.header("Agent Revocation")
    agents = am.load_agents()
    active_ids = [a_id for a_id, a in agents.items() if a["status"] == "Active"]

    if not active_ids:
        st.info("There are no active agents to revoke.")
    else:
        selected = st.selectbox(
            "Select an active agent to revoke", active_ids,
            format_func=lambda a_id: "{} \u2013 {} ({})".format(
                a_id, agents[a_id]["customer_name"], agents[a_id]["permission_level"]),
        )
        st.warning("After revocation, this agent will be BLOCKED from every action (Rule 2).")
        if st.button("Revoke selected agent"):
            try:
                record = am.revoke_agent(selected)
                al.log_event(
                    al.new_request_id(), record["revoked_at"], record["agent_id"],
                    record["customer_name"], "Revoke an AI agent", "-", 0, DECISION_ALLOW,
                    "Customer revoked the agent in the app.", 8, "Not required",
                    requested_by="Customer (app)",
                )
                st.success("Agent {} revoked on {}.".format(record["agent_id"], record["revoked_at"]))
            except ValueError as error:
                st.error(str(error))

    st.subheader("All agents")
    agents = am.load_agents()
    st.dataframe(pd.DataFrame(list(agents.values())), width="stretch", hide_index=True)

# ---------------------------------------------------------------------------
# D + E. SHOPPING REQUEST SIMULATOR and DECISION ENGINE output
# ---------------------------------------------------------------------------
elif page == "D. Shopping Request Simulator":
    st.header("Shopping Request Simulator")
    st.caption("Pretend to be an AI agent. Fill in the request and send it to the Gatekeeper.")

    agents = am.load_agents()

    def update_amount():
        product = st.session_state["sim_product"]
        if product in CATALOG:
            st.session_state["sim_amount"] = float(CATALOG[product])

    st.session_state.setdefault("sim_amount", float(CATALOG["Wireless Earbuds"]))

    c1, c2 = st.columns(2)
    with c1:
        default_agent = next(iter(agents), "AGT-001")
        agent_id = st.text_input("Agent ID", value=default_agent,
                                 help="Registered IDs: " + ", ".join(agents.keys()) +
                                 ". Type any other ID (e.g. AGT-999) to test an unknown agent.")
        default_customer = agents[default_agent]["customer_name"] if default_agent in agents else ""
        customer = st.text_input("Customer name", value=default_customer)
        action = st.selectbox("Requested action", ALL_ACTIONS)
    with c2:
        product_choice = st.selectbox("Product name", list(CATALOG.keys()) + [OTHER_PRODUCT],
                                      key="sim_product", on_change=update_amount)
        custom_product = ""
        if product_choice == OTHER_PRODUCT:
            custom_product = st.text_input("Type the product name")
        amount = st.number_input("Transaction amount (\u20b9)", min_value=0.0, step=100.0, key="sim_amount",
                                 help="Used for place order, cancel, return and refund. "
                                      "Ignored for read-only actions.")
        d_col, t_col = st.columns(2)
        request_date = d_col.date_input("Request date", value=datetime.now().date())
        request_time = t_col.time_input("Request time", value=datetime.now().time().replace(microsecond=0))

    st.write("Catalogue: " + ", ".join("{} ({})".format(n, format_inr(p)) for n, p in CATALOG.items()))

    if st.button("Send request to Gatekeeper", type="primary"):
        product = custom_product.strip() if product_choice == OTHER_PRODUCT else product_choice
        timestamp = datetime.combine(request_date, request_time).strftime(TIME_FORMAT)
        if action in READ_ONLY_ACTIONS:
            amount = 0.0           # no money is involved in read-only actions
        request = {
            "agent_id": agent_id.strip(), "customer": customer.strip(), "action": action,
            "product": product or "-", "amount": amount, "timestamp": timestamp,
        }
        request_id, result = process_request(request)
        st.session_state["last_result"] = (request_id, result)

    if "last_result" in st.session_state:
        st.divider()
        st.subheader("Decision Engine result")
        show_decision(st.session_state["last_result"][1], st.session_state["last_result"][0])
        if st.session_state["last_result"][1]["decision"] == DECISION_ASK:
            st.info("This request is waiting. Go to **F. Customer Confirmation** to confirm or reject it.")

# ---------------------------------------------------------------------------
# F. CUSTOMER CONFIRMATION
# ---------------------------------------------------------------------------
elif page == "F. Customer Confirmation":
    st.header("Customer Confirmation")
    pending = pm.load_pending()

    if not pending:
        st.info("No requests are waiting for confirmation.")
    for item in pending:
        req = item["request"]
        with st.container(border=True):
            st.subheader("Pending: {}".format(item["request_id"]))
            st.write("**Agent:** {}  |  **Customer:** {}".format(req["agent_id"], req["customer"]))
            st.write("**Action:** {}  |  **Product:** {}  |  **Amount:** {}".format(
                req["action"], req["product"], format_inr(float(req["amount"]))))
            st.caption("Requested at {}. This is above the {} limit, so your confirmation is required.".format(
                req["timestamp"], format_inr(SPENDING_LIMIT)))
            b1, b2, _ = st.columns([1, 1, 4])
            if b1.button("Confirm", key="confirm_" + item["request_id"], type="primary"):
                result = process_confirmation(item, "Confirmed")
                st.session_state["confirm_message"] = ("Confirmed", result)
                st.rerun()
            if b2.button("Reject", key="reject_" + item["request_id"]):
                result = process_confirmation(item, "Rejected")
                st.session_state["confirm_message"] = ("Rejected", result)
                st.rerun()

    if "confirm_message" in st.session_state:
        choice, result = st.session_state.pop("confirm_message")
        st.subheader("Last customer decision: {}".format(choice))
        show_decision(result)

# ---------------------------------------------------------------------------
# G. AUDIT LOG
# ---------------------------------------------------------------------------
elif page == "G. Audit Log":
    st.header("Audit Log")
    log_df = al.read_log()
    st.caption("Every request is recorded here (Rule 8). Newest first.")

    decisions = st.multiselect("Filter by decision", [DECISION_ALLOW, DECISION_ASK, DECISION_BLOCK],
                               default=[DECISION_ALLOW, DECISION_ASK, DECISION_BLOCK])
    shown = log_df[log_df["Decision"].isin(decisions)] if not log_df.empty else log_df
    st.dataframe(shown.iloc[::-1], width="stretch", hide_index=True)
    st.write("Rows shown: {} of {}".format(len(shown), len(log_df)))

    st.download_button(
        "Download audit log as CSV", data=al.log_as_csv_bytes(log_df),
        file_name="audit_log.csv", mime="text/csv",
    )

# ---------------------------------------------------------------------------
# H. SECURITY SUMMARY
# ---------------------------------------------------------------------------
elif page == "H. Security Summary":
    st.header("Security Summary")
    summary = al.request_summary(al.read_log())

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Allowed", summary["allowed"])
    c2.metric("Blocked", summary["blocked"])
    c3.metric("Sent for customer confirmation", summary["needed_confirmation"])
    c4.metric("Still waiting for customer", summary["pending"])

    if summary["total"] > 0:
        chart_df = pd.DataFrame(
            {"Requests": [summary["allowed"], summary["blocked"], summary["pending"]]},
            index=["Allowed", "Blocked", "Waiting for customer"],
        )
        st.bar_chart(chart_df)
        st.write("Out of **{}** requests: {:.0f}% allowed, {:.0f}% blocked, {:.0f}% waiting for the customer.".format(
            summary["total"], 100 * summary["allowed"] / summary["total"],
            100 * summary["blocked"] / summary["total"], 100 * summary["pending"] / summary["total"]))
        st.caption("Requests that were confirmed or rejected by the customer are counted under "
                   "Allowed or Blocked, and also under 'Sent for customer confirmation'.")
    else:
        st.info("No requests yet. Use the Shopping Request Simulator first.")

# ---------------------------------------------------------------------------
# TESTING RESULTS (six required test cases, run live)
# ---------------------------------------------------------------------------
elif page == "Testing Results":
    st.header("Testing Results \u2013 six required test cases")
    st.caption("These tests run on the real decision engine with a separate set of test agents. "
               "They do not change your audit log.")
    if st.button("Run the six test cases", type="primary"):
        st.session_state["test_rows"] = run_six_cases()

    if "test_rows" in st.session_state:
        rows = st.session_state["test_rows"]
        passed = sum(1 for r in rows if r["Result"] == "PASS")
        if passed == len(rows):
            st.success("{} of {} test cases passed.".format(passed, len(rows)))
        else:
            st.error("{} of {} test cases passed.".format(passed, len(rows)))
        st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)

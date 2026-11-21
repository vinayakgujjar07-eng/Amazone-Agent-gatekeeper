# Agent Gatekeeper – Online Shopping Security System

**Agent Gatekeeper: A Security and Authorization Framework for AI Agents in Online Shopping Platforms**

Agentic AI assignment · Category: **Online Store** · Reference company: Amazon

> \\\*\\\*Important:\\\*\\\* This is an independent academic prototype inspired by online shopping platforms.
> It is \\\*\\\*not\\\*\\\* connected to Amazon, and Amazon has not implemented, approved, or partnered with it.
> All customers, agents, products and prices are simulated. No real account, payment or personal data is used.

\---

## What it does

Agent Gatekeeper is a security checkpoint between a customer's **AI shopping agent** and an online store.
For every request it gives one of three decisions:

|Decision|Meaning|
|-|-|
|**ALLOW**|The action is permitted|
|**ASK CUSTOMER**|The customer must confirm first|
|**BLOCK**|The action is prohibited|

Supported activities: view product details, view product prices, view order history, place an order,
cancel an order, request a return, request a refund, register an AI agent, revoke an AI agent.
All amounts are in Indian Rupees (₹). The spending limit is **₹5,000**.

## The 8 security rules (checked in this order)

|#|Rule|Decision|
|-|-|-|
|1|Unknown agent|BLOCK|
|2|Revoked agent|BLOCK|
|3|Out-of-scope or suspicious action (outside permission, wrong customer, invalid amount, agent trying to register/revoke agents)|BLOCK|
|4|Read-only action by a registered, active agent|ALLOW|
|5|Money action up to ₹5,000|ALLOW|
|6|Money action above ₹5,000|ASK CUSTOMER|
|7|Customer confirmation recorded (Confirm → ALLOW, Reject → BLOCK)|ALLOW / BLOCK|
|8|Every request is written to the audit log|Applies to all|

The engine stops at the **first** rule that applies. Rules 1 and 2 come first, so a revoked agent can never bypass the system.

\---

## How to run on Windows (step by step)

1. **Install Python 3.10 or newer** from https://www.python.org/downloads/ . During installation, tick **"Add python.exe to PATH"**.
2. Open the **AgentGate** folder in File Explorer, click the address bar, type `cmd` and press Enter.
3. Create a virtual environment (recommended):

```
   python -m venv venv
   venv\\\\Scripts\\\\activate
   ```

4. Install the requirements:

```
   pip install -r requirements.txt
   ```

5. Start the app:

```
   streamlit run app.py
   ```

Your browser opens at http://localhost:8501 . (If asked for an email by Streamlit, just press Enter.)

6. To stop the app, press `Ctrl + C` in the command window.

### Run the tests

```
python tests/test\\\_gatekeeper.py
```

This prints the six required test cases with the actual result of each, saves `tests/test\\\_results.csv`,
and then runs the extra automated tests. The tests use temporary files and do not change your real data.

### Rebuild the two-page report (optional)

```
pip install reportlab pypdf
python report/build\\\_report.py --github https://github.com/YOUR-NAME/AgentGate --enrollment YOUR-NUMBER
```

\---

## Project structure

```
AgentGate/
├── app.py               Streamlit user interface (all sections A–H + test results page)
├── decision\\\_engine.py   The 8 rules and evaluate\\\_request()  <- the "brain"
├── agent\\\_manager.py     Register / revoke agents (data/agents.json)
├── audit\\\_logger.py      Audit log (data/audit\\\_log.csv) and summary counts
├── pending\\\_manager.py   Requests waiting for customer confirmation
├── test\\\_cases.py        The six required test cases (run on the real engine)
├── requirements.txt
├── README.md
├── PROMPTS.md
├── data/
│   ├── agents.json      Demo agents (simulated)
│   └── audit\\\_log.csv    Audit log
├── tests/
│   ├── test\\\_gatekeeper.py
│   └── test\\\_results.csv Created when you run the tests
├── screenshots/         Your screenshots (you capture these)
├── report/
│   ├── Report.pdf       Two-page academic report
│   └── build\\\_report.py
└── video/               Your demo video or its link
```

## How the code works (for your live demo)

1. **`app.py`** collects the request in the *Shopping Request Simulator* and calls `process\\\_request()`.
2. `process\\\_request()` calls **`evaluate\\\_request()`** in `decision\\\_engine.py`.
3. `evaluate\\\_request()` looks up the agent and goes through the rules in order (Rule 1, 2, 3 → block; Rule 4 → allow read-only; Rule 5 → allow within limit; Rule 6 → ask customer).
4. The result is written to the audit log by **`audit\\\_logger.log\\\_event()`** (Rule 8).
5. If the answer is **ASK CUSTOMER**, the request is saved in `data/pending\\\_requests.json`.
6. On the *Customer Confirmation* page the customer clicks **Confirm** or **Reject**. The engine runs again with that answer (Rule 7). If the agent was revoked while waiting, it is blocked (Rule 2), even if the customer clicked Confirm.
7. The audit log keeps **both** rows (the ASK CUSTOMER row and the final row) with the same Request ID, so history is never overwritten.

### Design choices you can explain

* **₹5,000 limit:** high enough for everyday purchases, low enough to limit the damage of a mistake, and it makes the demo clear (₹2,000 below; ₹8,000 and ₹10,000 above). Exactly ₹5,000 is allowed; only amounts *above* it need confirmation.
* **Permission levels:** *Read-only* agents can only view; *Full shopping* agents can also place, cancel, return and refund. This is what Rule 3 checks.
* **Register/Revoke:** done by the customer in the app (and logged). If an *AI agent* tries to register or revoke agents, Rule 3 blocks it.
* **Dashboard counts:** each agent request is counted once, using its latest decision.

## Limitations

Simulated data only; no real identity verification (anyone can type an agent ID); one global limit;
JSON/CSV files instead of a secure database; the confirmation screen is a simple button, not real customer authentication.




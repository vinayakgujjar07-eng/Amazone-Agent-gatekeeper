# PROMPTS.md – AI assistance used in this project

**Project:** Agent Gatekeeper – Online Shopping Security System (Agentic AI assignment, category: Online Store)
**AI assistant used:** Claude (Anthropic), in a chat conversation
**Independent academic prototype. Not connected to Amazon or any real customer account.**

## How the AI was used (honest summary)

The whole project was started from **one master prompt** (the assignment instructions, written as a phased plan) followed by a
short follow-up prompt. The AI produced the first version of the code, tests, report generator and documents.
The sections below show which part of the master prompt covered each topic. They are copied or shortened from the real prompt text.

> If you (the student) used any additional prompts, add them under the matching heading. Only list prompts you really used.

---

## 1. Initial project development prompt

> "Act as an expert in Agentic AI, software development, business analysis, cybersecurity, and academic project preparation.
> I am an MBA student pursuing Pharmaceutical and Healthcare Management with a minor in Business Analytics. … My assigned category is
> ONLINE STORE … Help me complete this assignment from beginning to end … Use simple English, easy explanations, practical examples, and
> beginner-friendly technical implementation. … Project title: 'Agent Gatekeeper: A Security and Authorization Framework for AI Agents in
> Online Shopping Platforms'. Reference company: Amazon. This is an independent academic prototype … Do not claim that Amazon has implemented,
> approved, or partnered with this prototype. … Work in seven phases (explain; design; build; install/run on Windows; test; report and PROMPTS.md;
> GitHub, screenshots, video and ZIP)."

**Follow-up prompt:** "Complete Phase 2 to Phase 7 in One go. Then provide me with result and report."

## 2. User interface development prompt

> "Develop a functional web-based application named 'Agent Gatekeeper – Online Shopping Security System'. Technology: Python, Streamlit, Pandas,
> JSON or CSV. Keep it beginner-friendly and easy to run on Windows. Sections: A. Dashboard, B. Agent Registration, C. Agent Revocation,
> D. Shopping Request Simulator, E. Decision Engine, F. Customer Confirmation, G. Audit Log (view and download as CSV), H. Security Summary.
> The application must work without connecting to Amazon or any real customer account. Use simulated shopping data."

## 3. Decision engine prompt

> "Create eight simple security rules covering registered agents, unknown agents, read-only activities, shopping transactions, spending limits,
> customer confirmation, agent revocation, and unauthorized or suspicious activities. Read-only actions from registered agents should be ALLOWED.
> Unknown agents must always be BLOCKED. Money actions below the limit can be ALLOWED if otherwise authorized. Above the limit: ASK CUSTOMER.
> Revoked agents must always be BLOCKED. Customer confirmation must be recorded before an above-limit transaction is authorized. An agent must not
> act outside its permitted authorization. Every request must be recorded in an audit log. Implement the rules in a clear priority order so that a
> revoked agent cannot bypass the security system. Use ₹ and set the initial spending limit at ₹5,000; explain why."

## 4. Agent registration and revocation prompt

> "B. Agent Registration: register a new AI agent, assign an agent ID, enter customer name, set agent status, display registered agents.
> C. Agent Revocation: select an existing AI agent, revoke its authorization, record the revocation date and time, and prevent revoked agents from
> performing further actions."

## 5. Audit logging prompt

> "G. Audit Log: maintain a record of every request with date and time, agent ID, requested action, product name, amount, decision, reason, rule number,
> and customer confirmation status. Allow users to view and download the audit log as CSV. H. Security Summary: display how many requests were allowed,
> blocked, and sent for customer confirmation."

## 6. Testing prompt

> "Create and execute at least six test cases: (1) registered agent checks prices → ALLOW; (2) unknown agent places an order → BLOCK; (3) registered agent
> buys a ₹10,000 product with a ₹5,000 limit → ASK CUSTOMER; (4) registered agent buys a ₹2,000 product → ALLOW; (5) revoked agent places an order → BLOCK;
> (6) registered agent requests a ₹8,000 refund → ASK CUSTOMER. For each test give the number, scenario, input, expected result, actual result, pass/fail and
> explanation. Actually execute the tests against the implemented decision engine. Do not invent successful test results."

---

## My Own Contribution

> **Read this first:** Write in this section **only what you really did yourself.** The AI did not make any of the changes below for you, and it cannot
> know what you have reviewed or changed. Fill in the table and delete the lines that are not true. Your GitHub commit history should show your own work
> honestly, on the real dates when you did it.

### A. Review and testing (tick only what you really did)

- [ ] I read every file and can explain `decision_engine.py` rule by rule.
- [ ] I ran the app on my own computer with `streamlit run app.py`.
- [ ] I ran `python tests/test_gatekeeper.py` and saw the six required tests pass.
- [ ] I tried extra requests in the simulator (for example exactly ₹5,000 and ₹5,001).
- [ ] I tested revoking an agent while a request was waiting for confirmation.
- [ ] I captured the screenshots and recorded the video myself.

### B. Changes I made myself (fill in)

| # | What I changed or added | Why | File(s) | Date | Commit message |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

### C. Suggestions for meaningful modifications you can make yourself

Pick two or three, do them yourself, test them, and then describe them in table B.

1. **Change the spending limit** (for example to ₹3,000) and update the tests and the report. Explain why you chose the new number.
2. **Per-agent spending limit:** add a `spending_limit` field to each agent in `agents.json`, and make Rule 5/6 use it instead of the single global limit.
3. **Daily spending total:** block or ask the customer when an agent's total spending in one day goes above a daily limit.
4. **New permission level** (for example *Orders only, no refunds*) and a test case for it.
5. **Use your own pharmacy-related product catalogue** (for example health-care products) in the simulator, and mention it in the report.
6. **Add three more test cases** of your own (for example a ₹5,000 order, a cancel of ₹9,000, a read-only agent trying to refund) and report the results.
7. **Add a column or filter** to the audit log, for example filter by agent ID or by date.
8. **Improve the wording** of the decision reasons so that they sound natural to you, and check that the tests still pass.
9. **Add an input check** in the app (for example a maximum amount) and explain what problem it prevents.

### D. What I can explain in my viva

(Write 3–5 sentences in your own words: why the rules are in this order, what happens when a customer confirms, and what the limitations are.)

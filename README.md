# \# Amazon Agent Gatekeeper

# 

# \*\*An AI Governance \& Consumer Protection Platform for Autonomous E-Commerce Agents\*\*  

# \*Academic MBA Project | Reference Company: Amazon | Technologies: Python, Streamlit, Pandas\*

# 

# \---

# 

# \## 1. Project Introduction

# 

# The \*\*Amazon Agent Gatekeeper\*\* is a web-based supervisory system designed to control and govern the actions of autonomous personal AI shopping agents. 

# 

# As artificial intelligence advances from conversational chatbots to autonomous agents capable of executing transactions on behalf of consumers (such as automated grocery replenishment, deal-monitoring bots, or gift shoppers), consumers face new operational and financial risks. 

# 

# The Agent Gatekeeper acts as an automated, policy-enforcing firewall between personal AI agents and the Amazon checkout infrastructure. By evaluating incoming agent requests against multi-tiered governance rules, the Gatekeeper ensures that autonomous shopping remains safe, bounded, and transparent while preserving consumer convenience.

# 

# \---

# 

# \## 2. Business Problem

# 

# In classical economic theory, the \*\*Principal-Agent Problem\*\* arises when an individual (the principal) delegates authority to another entity (the agent) who may act with imperfect information, conflicting incentives, or unpredictable behavior. In autonomous e-commerce:

# 

# \* \*\*The Principal:\*\* The consumer (account owner) who wants convenience, budget discipline, and authentic products.

# \* \*\*The Agent:\*\* Autonomous AI software bots instructed to monitor prices, restock household items, or find deals.

# 

# Without a supervisory governance layer, delegating purchasing authority creates critical business risks:

# 

# 1\. \*\*Runaway Financial Spending:\*\* Autonomous agents caught in repetitive loops or misunderstanding price drops can exhaust credit limits or deplete bank balances.

# 2\. \*\*Category Scope Creep:\*\* An AI agent intended only for routine grocery replenishment might purchase luxury apparel, electronics, or digital gift cards.

# 3\. \*\*Merchant \& Counterfeit Fraud:\*\* Agents prioritizing low prices or high availability may inadvertently order from unverified, newly registered, or blacklisted marketplace sellers.

# 4\. \*\*Adversarial Threats \& Prompt Injection:\*\* Malicious seller listings or external prompt injection attacks can attempt to instruct the AI agent to bypass spending limits or transfer funds.

# 5\. \*\*Loss of Consumer Sovereignty:\*\* When shopping becomes fully automated, consumers lose direct visibility over what is purchased until packages arrive at their door.

# 

# \---

# 

# \## 3. Project Objectives

# 

# The primary objectives of the Amazon Agent Gatekeeper project are:

# 

# 1\. \*\*Establish a Guardrail Boundary:\*\* Enforce a strict financial policy limit where routine purchases up to \*\*₹5,000\*\* can execute autonomously, while larger purchases require human approval.

# 2\. \*\*Implement Three Deterministic Decisions:\*\*

# &#x20;  - \*\*`ALLOW`\*\*: Permit autonomous checkout when transactions are compliant and low-risk.

# &#x20;  - \*\*`ASK CUSTOMER`\*\*: Escalate transactions to an interactive Human-in-the-Loop (HITL) queue when spending limits are exceeded or seller risks are elevated.

# &#x20;  - \*\*`BLOCK`\*\*: Stop unauthorized, malicious, or policy-violating purchase attempts immediately.

# 3\. \*\*Enforce Least-Privilege Scope:\*\* Restrict each agent to designated product categories (e.g., Grocery \& Pantry, Electronics, Books).

# 4\. \*\*Provide Consumer Kill-Switches:\*\* Allow the account holder to suspend, reactivate, or permanently revoke an agent's authority at any time.

# 5\. \*\*Maintain Immutable Auditability:\*\* Record every decision, rule trigger, and customer confirmation in a structured ledger to support dispute resolution and compliance.

# 

# \---

# 

# \## 4. System Overview \& Architecture

# 

# The Gatekeeper functions as an intermediate policy evaluation layer. When an AI agent generates a checkout request, the request is intercepted and evaluated across a sequential \*\*6-Stage Policy Pipeline\*\* before reaching fulfillment:

# 

# ```

# \[Personal AI Agent] 

# &#x20;      │  (dispatches shopping request)

# &#x20;      ▼

# ┌──────────────────────────────────────────────────────────┐

# │             AMAZON AGENT GATEKEEPER ENGINE              │

# │                                                          │

# │  Stage 1: Zero-Trust Agent Lifecycle Gate                │

# │           (Active vs. Suspended vs. Revoked)             │

# │  Stage 2: Operational Scope / Category Whitelist Gate    │

# │           (Authorized product categories)                │

# │  Stage 3: Adversarial Intent \& Prompt Injection Gate     │

# │           (Detection of override/bypass tokens)          │

# │  Stage 4: Marketplace Merchant Trust \& Reputation Gate   │

# │           (Prime, Verified Brand, New, Flagged)          │

# │  Stage 5: Financial Guardrail Gate (₹5,000 Threshold)   │

# │           (Per-transaction ceiling \& overspend check)    │

# │  Stage 6: Velocity \& Cumulative Daily Budget Gate        │

# │           (Rolling calendar-day spend consumption)       │

# └──────────────────────────┬───────────────────────────────┘

# &#x20;                          │

# &#x20;      ┌───────────────────┼───────────────────┐

# &#x20;      ▼                   ▼                   ▼

# &#x20; 🟢 \[ALLOW]        🟡 \[ASK CUSTOMER]      🔴 \[BLOCK]

# Autonomous Order       Held in Human-        Immediate Security

# &#x20;Dispatched to          in-the-Loop          Termination; Zero

# &#x20; Fulfillment         Approval Queue         Capital Exposure

# ```

# 

# \### The Three Decision Outcomes

# 

# | Decision | Visual Badge | Execution Mode | Business Condition | System Action |

# | :--- | :---: | :---: | :--- | :--- |

# | \*\*`ALLOW`\*\* | 🟢 Emerald | Autonomous | Amount ≤ ₹5,000, agent active, authorized category, verified seller, within daily budget. | Dispatches order with zero customer friction; logs to audit trail. |

# | \*\*`ASK CUSTOMER`\*\* | 🟡 Amber | Human-in-the-Loop | Amount > ₹5,000 (up to ₹10,000), agent per-tx cap exceeded, or unverified merchant. | Places order on hold in confirmation queue awaiting explicit customer sign-off. |

# | \*\*`BLOCK`\*\* | 🔴 Crimson | Hard Security Stop | Agent revoked/suspended, unauthorized category, gross overspend (> ₹10,000), flagged seller, or prompt injection. | Terminates transaction immediately; zero funds deducted; logs security breach. |

# 

# \---

# 

# \## 5. Application Features

# 

# The application provides an enterprise-style AI governance dashboard across eight core sections:

# 

# 1\. \*\*Executive Dashboard (`views/dashboard.py`):\*\*

# &#x20;  - Live KPI cards tracking total requests, decision counts (`ALLOW`, `ASK CUSTOMER`, `BLOCK`), and financial exposure prevented.

# &#x20;  - Interactive Plotly charts for decision distribution and spend by product category.

# &#x20;  - Real-time agent fleet health cards and daily budget consumption progress meters.

# 

# 2\. \*\*Agent Registration \& Delegated Authority (`views/agent\_registration.py`):\*\*

# &#x20;  - Onboards new personal AI agents with unique system IDs (e.g., `AGT-101`).

# &#x20;  - Assigns friendly names, ownership tags, operational mandates, and autonomy tiers.

# &#x20;  - Restricts agents to designated product categories using least-privilege principles.

# &#x20;  - Enforces visible financial guardrails (per-transaction caps under ₹5,000 and daily budget ceilings).

# 

# 3\. \*\*Agent Revocation \& Kill Switch (`views/agent\_revocation.py`):\*\*

# &#x20;  - Displays real-time operational status (Active 🟢, Suspended 🟡, Revoked 🔴).

# &#x20;  - Provides three separate lifecycle actions:

# &#x20;    - \*\*Suspend Agent:\*\* Temporary operational pause (e.g., during vacation).

# &#x20;    - \*\*Reactivate Agent:\*\* Restores active purchasing authority.

# &#x20;    - \*\*Emergency Kill Switch (Revoke):\*\* Permanently invalidates credentials with mandatory justification notes.

# 

# 4\. \*\*Shopping Request Simulator (`views/shopping\_simulator.py`):\*\*

# &#x20;  - Pre-configured 1-click execution for eight curated MBA policy scenarios.

# &#x20;  - \*\*Batch Regression Suite Runner:\*\* Executes all eight scenarios simultaneously and generates a test verification matrix.

# &#x20;  - Custom Agent Request Builder allowing users to select catalogue products or input arbitrary prices, merchants, and agent prompts.

# &#x20;  - Color-coded evaluation result cards detailing the decision, reason, rules triggered, risk score, and test outcome.

# 

# 5\. \*\*Decision Engine \& Policy Matrix (`views/decision\_engine\_view.py`):\*\*

# &#x20;  - Educational inspection of the 6-stage policy pipeline and decision criteria.

# &#x20;  - Interactive Policy Sandbox with real-time sliders to observe decision outputs and risk score transitions.

# 

# 6\. \*\*Customer Confirmation / HITL Review (`views/customer\_confirmation.py`):\*\*

# &#x20;  - Clean, container-based transaction cards for orders requiring customer confirmation.

# &#x20;  - Displays product name, amount in Indian Rupees (₹), requesting agent, fulfilling seller, risk score gauge, and escalation reason.

# &#x20;  - Provides three explicit customer actions:

# &#x20;    1. \*\*Approve Purchase:\*\* Confirms order and dispatches it to fulfillment.

# &#x20;    2. \*\*Reject Purchase:\*\* Declines purchase without deducting funds.

# &#x20;    3. \*\*Reject \& Revoke Agent:\*\* Declines purchase and triggers an immediate kill switch to revoke the agent.

# 

# 7\. \*\*Comprehensive Audit Log (`views/audit\_log\_view.py`):\*\*

# &#x20;  - Searchable, filterable event ledger backed by Pandas.

# &#x20;  - Multi-criteria filtering by decision, status, agent, keyword, and transaction amount.

# &#x20;  - Forensic Transaction Inspector displaying detailed policy rule traces.

# &#x20;  - 1-Click export to CSV and JSON formats.

# 

# 8\. \*\*Security Summary \& MBA Governance Report (`views/security\_summary.py`):\*\*

# &#x20;  - Strategic Key Risk Indicators (KRIs) including compliance rate, escalation rate, block rate, and capital protected.

# &#x20;  - Pareto analysis of policy violation drivers and agent trustworthiness ratings.

# &#x20;  - Academic business analysis mapping governance to the \*\*Three Lines of Defense\*\* framework and global AI regulations.

# 

# \---

# 

# \## 6. Eight Governance Scenarios

# 

# The simulator includes eight predefined scenarios designed to demonstrate governance rules across normal, edge-case, and adversarial conditions:

# 

# | Scenario | Scenario Title | Agent ID | Product \& Amount (₹) | Fulfilling Merchant | Expected Decision | Governance Principle Tested |

# | :---: | :--- | :---: | :--- | :--- | :---: | :--- |

# | \*\*A\*\* | \*\*Routine Grocery Refill\*\* | `AGT-101` | Aashirvaad Atta 10kg  <br/>\*\*₹499.00\*\* | Amazon Fulfilled (Prime) | \*\*`ALLOW`\*\* | \*\*Compliant Routine Purchase:\*\* Essential item below ₹5,000 threshold within authorized grocery scope and verified seller. |

# | \*\*B\*\* | \*\*Smart Speaker Deal\*\* | `AGT-102` | Echo Dot (5th Gen)  <br/>\*\*₹4,499.00\*\* | Amazon Fulfilled (Prime) | \*\*`ALLOW`\*\* | \*\*High-Value Compliant Purchase:\*\* Order near the policy limit (₹4,499 ≤ ₹5,000) by an active agent with authorized electronics scope and Prime fulfillment. |

# | \*\*C\*\* | \*\*Purchase Exceeding Limit\*\* | `AGT-102` | Fire TV Stick 4K  <br/>\*\*₹5,999.00\*\* | Amazon Fulfilled (Prime) | \*\*`ASK CUSTOMER`\*\* | \*\*Spending Threshold Escalation:\*\* Amount exceeds the ₹5,000 limit, requiring explicit Human-in-the-Loop customer confirmation. |

# | \*\*D\*\* | \*\*Critical Overspend\*\* | `AGT-102` | Sony ANC Headphones  <br/>\*\*₹26,990.00\*\* | Verified Brand Store | \*\*`BLOCK`\*\* | \*\*Hard Safety Ceiling Breach:\*\* Amount breaches 2x spending limit (> ₹10,000), triggering an automatic block to prevent severe financial exposure. |

# | \*\*E\*\* | \*\*Scope Violation\*\* | `AGT-101` | Luxury Replica Watch  <br/>\*\*₹4,800.00\*\* | High-Risk / Flagged Seller | \*\*`BLOCK`\*\* | \*\*Least-Privilege Boundary:\*\* Grocery agent attempting a Fashion purchase combined with a blacklisted counterfeit seller. |

# | \*\*F\*\* | \*\*Revoked Agent\*\* | `AGT-105` | Amazon Prime Membership  <br/>\*\*₹1,499.00\*\* | Amazon Fulfilled (Prime) | \*\*`BLOCK`\*\* | \*\*Zero-Trust Credential Gate:\*\* Intercepts checkout requests from decommissioned or revoked agent credentials. |

# | \*\*G\*\* | \*\*Unverified Merchant\*\* | `AGT-101` | Optimum Nutrition Whey  <br/>\*\*₹4,199.00\*\* | New / Unverified Merchant | \*\*`ASK CUSTOMER`\*\* | \*\*Merchant Trust Escalation:\*\* Order > ₹2,000 from a newly registered merchant with limited seller reputation. |

# | \*\*H\*\* | \*\*Prompt Injection Attack\*\* | `AGT-102` | Apple 20W Power Adapter  <br/>\*\*₹1,899.00\*\* | Verified Brand Store | \*\*`BLOCK`\*\* | \*\*Adversarial Threat Shield:\*\* Intercepts subversive prompt instructions attempting to bypass gatekeeper limits. |

# 

# \---

# 

# \## 7. Technology Stack

# 

# \* \*\*Programming Language:\*\* Python 3.10+ (tested and verified on Python 3.14)

# \* \*\*Web UI Framework:\*\* Streamlit (`streamlit >= 1.28.0`)

# \* \*\*Data Processing \& Analytics:\*\* Pandas (`pandas >= 2.0.0`)

# \* \*\*Interactive Charting:\*\* Plotly (`plotly >= 5.15.0`)

# \* \*\*Data Storage:\*\* Local JSON-backed persistence (`data/agents.json`, `data/products.json`, `data/transactions.json`)

# 

# \---

# 

# \## 8. Installation Instructions

# 

# \### Step 1: Verify Python Installation

# Ensure Python 3.10 or higher (such as Python 3.14) is installed:

# ```bash

# python --version

# \# or on Windows:

# py -3.14 --version

# ```

# 

# \### Step 2: Navigate to Project Directory

# ```bash

# cd "c:\\Users\\Vinayak Gujjar\\Desktop\\Agent Gate"

# ```

# 

# \### Step 3: Install Required Dependencies

# Install the required packages using pip:

# ```bash

# py -3.14 -m pip install -r requirements.txt

# \# or standard pip:

# pip install -r requirements.txt

# ```

# 

# \---

# 

# \## 9. How to Run the Application

# 

# \### Option A: Standard Command (Python 3.14)

# From the project folder, execute:

# ```bash

# py -3.14 -m streamlit run app.py

# ```

# 

# \### Option B: General Streamlit Command

# ```bash

# streamlit run app.py

# ```

# 

# \### Option C: 1-Click Windows Launcher

# Double-click `run\_app.bat` in the project root directory.

# 

# Once launched, the application opens in your default web browser at:

# ```

# http://localhost:8501

# ```

# 

# \### Option D: Run Automated Regression Suite

# To run the automated validation test verifying all eight scenarios and data models:

# ```bash

# py -3.14 test\_regression\_suite.py

# ```

# 

# \---

# 

# \## 10. Business Benefits

# 

# 1\. \*\*Consumer Capital Protection:\*\*

# &#x20;  - Limits financial exposure to a maximum of ₹5,000 per autonomous transaction.

# &#x20;  - Prevents catastrophic loss from rogue agent behavior, system loops, or compromised credentials.

# 

# 2\. \*\*Preserved Convenience for Routine Shopping:\*\*

# &#x20;  - Over 80% of routine household restocking (flour, oil, tea, paperbacks) falls below ₹5,000 and executes autonomously without human friction.

# 

# 3\. \*\*Enhanced Platform Trust \& Adoption:\*\*

# &#x20;  - E-commerce platforms like Amazon can accelerate adoption of autonomous shopping agents by assuring consumers that agents cannot make unauthorized high-value purchases.

# 

# 4\. \*\*Regulatory Alignment \& Compliance:\*\*

# &#x20;  - \*\*EU Artificial Intelligence Act (Article 14 - Human Oversight):\*\* Implements meaningful Human-in-the-Loop oversight and emergency kill switches for automated financial systems.

# &#x20;  - \*\*India Digital Personal Data Protection (DPDP) Act 2023 \& Consumer Protection Act 2019:\*\* Prevents unfair automated debits, enforces delegated scope limits, and maintains immutable event records.

# 

# \---

# 

# \## 11. Project Limitations

# 

# 1\. \*\*Simulated Marketplace Data:\*\*

# &#x20;  - The application uses simulated Amazon India product catalogues, synthetic agents, and mock order requests. It does not connect to live Amazon production accounts or actual banking payment gateways.

# 2\. \*\*Deterministic Heuristic Rules:\*\*

# &#x20;  - Policy evaluations rely on deterministic threshold checks, category whitelists, and regex pattern matching rather than deep-learning natural language understanding models.

# 3\. \*\*Single-User Scope:\*\*

# &#x20;  - Designed as a personal account governance prototype. It does not include enterprise multi-tenant access control or organization-wide role hierarchies.

# 4\. \*\*Local File Persistence:\*\*

# &#x20;  - Transaction records and agent rosters are persisted in local JSON files rather than distributed enterprise databases (such as PostgreSQL or Amazon DynamoDB).

# 

# \---

# 

# \## 12. Academic Citation \& Attribution

# 

# \* \*\*Project Title:\*\* Amazon Agent Gatekeeper

# \* \*\*Academic Discipline:\*\* Master of Business Administration (MBA) - Technology Management \& Information Systems

# \* \*\*Reference Company:\*\* Amazon.com, Inc. / Amazon India

# \* \*\*Framework Reference:\*\* Agency Theory (Jensen \& Meckling, 1976), Three Lines of Defense in Risk Management (IIA), EU AI Act (Article 14).




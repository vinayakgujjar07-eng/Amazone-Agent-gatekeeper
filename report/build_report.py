"""
report/build_report.py
======================
Builds report/Report.pdf (maximum TWO pages).

The testing table is filled by RUNNING the six test cases against the decision
engine, so the report always shows real results.

Usage (from the AgentGate folder):
    pip install reportlab
    python report/build_report.py --github https://github.com/YOUR-NAME/AgentGate --enrollment 12345678

If you do not pass --github, the report shows a visible reminder to add it.
"""

import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from reportlab.lib import colors                                   # noqa: E402
from reportlab.lib.enums import TA_JUSTIFY                         # noqa: E402
from reportlab.lib.pagesizes import A4                             # noqa: E402
from reportlab.lib.styles import ParagraphStyle                    # noqa: E402
from reportlab.lib.units import mm                                 # noqa: E402
from reportlab.pdfbase import pdfmetrics                           # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                       # noqa: E402
from reportlab.platypus import (KeepTogether, Paragraph, SimpleDocTemplate, Spacer,   # noqa: E402
                                Table, TableStyle)

from decision_engine import RULES, SPENDING_LIMIT                  # noqa: E402
from test_cases import run_six_cases                               # noqa: E402

# ---------------------------------------------------------------------------
# Fonts: use a font that has the rupee sign. If none is found, write "Rs." instead.
# ---------------------------------------------------------------------------
FONT_CANDIDATES = [
    ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    ("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/arialbd.ttf"),
    ("C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/segoeuib.ttf"),
]
BASE, BOLD, RS = "Helvetica", "Helvetica-Bold", "Rs. "
for regular, bold in FONT_CANDIDATES:
    if os.path.exists(regular) and os.path.exists(bold):
        pdfmetrics.registerFont(TTFont("ReportFont", regular))
        pdfmetrics.registerFont(TTFont("ReportFont-Bold", bold))
        pdfmetrics.registerFontFamily("ReportFont", normal="ReportFont", bold="ReportFont-Bold",
                                      italic="ReportFont", boldItalic="ReportFont-Bold")
        BASE, BOLD, RS = "ReportFont", "ReportFont-Bold", "\u20b9"
        break

FS = 9.0   # body font size

body = ParagraphStyle("body", fontName=BASE, fontSize=FS, leading=FS + 2.2, alignment=TA_JUSTIFY, spaceAfter=2)
h1 = ParagraphStyle("h1", fontName=BOLD, fontSize=13, leading=15, spaceAfter=1)
sub = ParagraphStyle("sub", fontName=BASE, fontSize=8, leading=10, textColor=colors.HexColor("#444444"), spaceAfter=3)
h2 = ParagraphStyle("h2", fontName=BOLD, fontSize=9.4, leading=11, spaceBefore=4, spaceAfter=1.5,
                    textColor=colors.HexColor("#0B3D6B"))
cell = ParagraphStyle("cell", fontName=BASE, fontSize=7.8, leading=9.4)
cell_b = ParagraphStyle("cell_b", fontName=BOLD, fontSize=7.8, leading=9.4, textColor=colors.white)
ref = ParagraphStyle("ref", fontName=BASE, fontSize=7.8, leading=9.6, leftIndent=9, firstLineIndent=-9, spaceAfter=1.2)


def P(text, style=body):
    return Paragraph(text, style)


def make_table(data, widths, header_color="#0B3D6B"):
    rows = []
    for r, row in enumerate(data):
        rows.append([P(str(c), cell_b if r == 0 else cell) for c in row])
    t = Table(rows, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(header_color)),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA5B1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F2F6FA")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 1.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.6),
        ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


def build(output_path, github, name, enrollment):
    limit = "{}{:,}".format(RS, SPENDING_LIMIT)
    results = run_six_cases()
    passed = sum(1 for r in results if r["Result"] == "PASS")

    doc = SimpleDocTemplate(output_path, pagesize=A4, leftMargin=14 * mm, rightMargin=14 * mm,
                            topMargin=11 * mm, bottomMargin=10 * mm,
                            title="Agent Gatekeeper - Academic Report", author=name)
    s = []
    width = A4[0] - 28 * mm

    # 1. Project title
    s.append(P("1. Agent Gatekeeper: A Security and Authorization Framework for AI Agents "
               "in Online Shopping Platforms", h1))
    s.append(P("Agentic AI assignment &nbsp;|&nbsp; Category: Online Store &nbsp;|&nbsp; MBA (Pharmaceutical and Healthcare "
               "Management), minor in Business Analytics &nbsp;|&nbsp; {} &nbsp;|&nbsp; Enrollment no.: {}<br/>"
               "GitHub: {}".format(name, enrollment, github), sub))

    # 2. Introduction
    s.append(P("2. Introduction", h2))
    s.append(P("Customers have started to use personal AI agents that can search for products, compare prices and even "
               "place orders. An agent that can act for a customer needs clear limits. This report describes "
               "<b>Agent Gatekeeper</b>, a small working prototype that acts like a security guard between an AI agent and "
               "an online shop. For every request it gives one of three decisions: <b>ALLOW</b>, <b>ASK CUSTOMER</b> or "
               "<b>BLOCK</b>. It is an independent academic prototype built with Python and Streamlit, using only simulated data."))

    # 3. Selected company
    s.append(P("3. Selected Company \u2013 Amazon", h2))
    s.append(P("Amazon is used as the reference company because it is a very large online store with orders, returns and refunds, "
               "and it is already testing AI shopping agents. TechCrunch [1] reported in April 2025 that Amazon was testing a "
               "\u201cBuy for Me\u201d agent with some users, which visits another website and fills in the customer\u2019s name, address and payment "
               "details to buy a product. Digital Commerce 360 [2] reported that Amazon said the customer stays in control of the agent. "
               "<b>This prototype is not connected to Amazon. Amazon has not implemented, approved or partnered with it.</b>"))

    # 4. Business problem
    s.append(P("4. Business Problem", h2))
    s.append(P("When an agent can buy or ask for refunds, the customer must trust it not to make mistakes and may have less control. "
               "TechCrunch [1] noted this, for example an agent ordering far more items than intended. Google\u2019s announcement of its "
               "Agent Payments Protocol (AP2) [3] explains that today\u2019s payment systems usually assume a person clicks \u201cbuy\u201d, and "
               "lists three open questions for agent payments: <i>authorization</i> (did the user allow this purchase?), <i>authenticity</i> "
               "(does the request match what the user wanted?) and <i>accountability</i> (who is responsible if something goes wrong?). "
               "Axios [4] also reports that AP2 is designed to prove that a user gave an agent authority for a specific purchase. "
               "In a shopping platform, the main risks are: (a) an agent buying expensive items without permission, (b) an unknown agent "
               "accessing customer information, (c) a revoked agent still placing orders, and (d) unauthorized refund requests."))

    # 5. Proposed solution
    s.append(P("5. Proposed Solution", h2))
    s.append(P("Agent Gatekeeper checks <b>every</b> request before it reaches the shop. It supports nine activities: view product details, "
               "prices and order history; place, cancel, return and refund orders; and register and revoke agents. All amounts are in "
               "Indian Rupees. The initial spending limit is <b>{limit}</b>. This is a demonstration choice: it is high enough for everyday "
               "purchases, so customers are not asked all the time, but low enough to limit the damage from a mistake, and it makes the "
               "test cases clear ({r}2,000 is below it; {r}8,000 and {r}10,000 are above it). A real system would let each customer set "
               "their own limit.".format(limit=limit, r=RS)))

    # 6. Security rules
    s.append(P("6. Security Rules (checked in this order; the first rule that applies decides)", h2))
    rule_rows = [["#", "Rule", "Decision", "Simple explanation"]]
    for n, r in RULES.items():
        rule_rows.append([n, r["title"], r["decision"], r["explanation"].replace("Rs. 5,000", limit)])
    s.append(make_table(rule_rows, [6 * mm, 36 * mm, 21 * mm, width - 63 * mm]))
    s.append(P("Unknown and revoked agents are checked first (Rules 1\u20132), so a revoked agent can never reach a rule that allows an action. "
               "An amount exactly equal to the limit is allowed; only amounts above it need confirmation.", body))

    # 7. Prototype functionality
    s.append(P("7. Prototype Functionality", h2))
    s.append(P("The web app has a dashboard (agent and request counts), agent registration, agent revocation with date and time, a shopping "
               "request simulator, a decision display (decision, reason, rule number, amount, agent status), a customer confirmation page "
               "with Confirm and Reject buttons, an audit log that can be downloaded as CSV, and a security summary. Agents are saved in a "
               "JSON file and the audit log in a CSV file. <b>How the decision engine works:</b> it looks up the agent, then goes through "
               "Rules 1 to 7 in order. For an above-limit request it returns ASK CUSTOMER and the request waits. When the customer answers, "
               "the engine checks the rules again (so an agent revoked in the meantime is still blocked) and only a recorded confirmation "
               "turns the result into ALLOW. Rule 8 means every decision is written to the audit log. "
               "<b>How it protects customers:</b> strangers and revoked agents are stopped, agents cannot act outside their permission or for "
               "another customer, large payments need the customer\u2019s approval, and everything can be checked later in the log."))

    # 8. Testing results
    test_heading = P("8. Testing Results", h2)
    test_rows = [["Test", "Scenario", "Expected", "Actual", "Result"]]
    for r in results:
        test_rows.append([r["Test"], r["Scenario"].replace("Rs. ", RS), r["Expected"], r["Actual"], r["Result"]])
    s.append(KeepTogether([test_heading, make_table(
        test_rows, [9 * mm, width - 9 * mm - 33 * mm - 33 * mm - 12 * mm, 33 * mm, 33 * mm, 12 * mm])]))
    s.append(P("The six required cases were run against the real decision engine: <b>{} of {} passed</b>. "
               "Extra automated tests (limit boundary, confirmation, rejection, revoked agent priority, read-only agents, wrong customer, invalid amount, "
               "audit log, registration and revocation) are in <i>tests/test_gatekeeper.py</i>.".format(passed, len(results)), body))

    # 9. Business benefits
    s.append(P("9. Business Benefits", h2))
    s.append(P("Customers keep control of spending and can withdraw an agent\u2019s access at any time. The store reduces disputes and fraud "
               "risk because every action has a clear rule and a record. The audit log supports accountability, and the rules are simple "
               "enough for managers to read, explain and change."))

    # 10. Limitations
    s.append(P("10. Limitations", h2))
    s.append(P("This is a prototype with simulated data and no real shop, payment or customer account. It does not prove who an agent really is "
               "(anyone can type an agent ID), unlike cryptographic approaches such as AP2 [3]. It uses one global limit, JSON/CSV files instead of a "
               "secure database, and a simple confirmation screen instead of real customer authentication. Return and refund amounts are entered by hand. "
               "It has not been tested with real AI agents or large numbers of users."))

    # 11. Conclusion
    s.append(P("11. Conclusion", h2))
    s.append(P("Agent Gatekeeper shows, in a simple and testable way, how an online store can let AI agents help customers without giving up "
               "control. Priority-ordered rules, customer confirmation above {} and a full audit log make agent shopping safer and easier to "
               "explain. Future work could add per-customer limits, real identity checks and integration with payment systems.".format(limit)))

    # 12. References
    s.append(P("12. References", h2))
    refs = [
        "[1] TechCrunch (3 April 2025). Amazon\u2019s new AI agent will shop third-party sites for you. "
        "https://techcrunch.com/2025/04/03/amazons-new-ai-agent-will-shop-third-party-stores-for-you",
        "[2] Digital Commerce 360 (8 April 2025). Amazon pilots \u2018Buy for Me\u2019 AI shopping tool. "
        "https://www.digitalcommerce360.com/2025/04/08/amazon-buy-for-me-agentic-ai-shopping-tool/",
        "[3] Parikh, S. and Surapaneni, R., Google Cloud Blog (16 September 2025). Powering AI commerce with the new Agent Payments Protocol (AP2). "
        "https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol",
        "[4] Axios (16 September 2025). Google\u2019s new plan to build trust in AI agents as personal shoppers. "
        "https://www.axios.com/2025/09/16/google-ai-agents-ecommerce-online-shopping",
    ]
    for r in refs:
        s.append(P(r, ref))

    doc.build(s)
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build the two-page Agent Gatekeeper report.")
    parser.add_argument("--github", default="[ADD YOUR GITHUB REPOSITORY LINK HERE]")
    parser.add_argument("--name", default="Vinayak")
    parser.add_argument("--enrollment", default="[add enrollment no.]")
    parser.add_argument("--out", default=os.path.join(ROOT, "report", "Report.pdf"))
    args = parser.parse_args()

    build(args.out, args.github, args.name, args.enrollment)

    try:
        from pypdf import PdfReader
        pages = len(PdfReader(args.out).pages)
        print("Report saved to {} ({} page(s)).".format(args.out, pages))
        if pages > 2:
            print("WARNING: the report is longer than two pages. Shorten the text.")
    except ImportError:
        print("Report saved to {}. Open it and check that it is two pages or fewer.".format(args.out))

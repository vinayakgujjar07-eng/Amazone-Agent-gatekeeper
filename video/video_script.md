# Video demonstration script (about 1 minute 45 seconds)

**You must record this yourself and speak in your own voice.** Change any words so that they sound natural to you.
Record your screen with the Windows Game Bar (press `Windows + G`, then the record button), or OBS Studio, or Zoom (share screen + record).

## Before recording (2 minutes)

1. Run `streamlit run app.py`.
2. In the sidebar open **Reset demo data**, tick the box and click **Reset now**. This gives you 3 clean demo agents and an empty log.
3. Open the **D. Shopping Request Simulator** page. Know the three demo agents:
   - `AGT-001` Rahul Verma – Active, Full shopping
   - `AGT-002` Rahul Verma – **Revoked**
   - `AGT-003` Priya Sharma – Active, Read-only

## Script

| Time | What you show | What you say (easy English) |
|---|---|---|
| 0:00–0:15 | Dashboard | "Hello, I am ___. This is Agent Gatekeeper, my Agentic AI project for the Online Store category. It is a security checkpoint between a customer's AI shopping agent and an online store. It gives one of three decisions: Allow, Ask Customer, or Block. This is an academic prototype inspired by Amazon, and it is not connected to Amazon." |
| 0:15–0:25 | Dashboard rules expander | "It uses eight rules, checked in priority order. Unknown and revoked agents are checked first, so they can never bypass the system. The spending limit is five thousand rupees." |
| 0:25–0:35 | **Test 1:** AGT-001, Rahul Verma, *View product prices* → Send | "Test 1. A registered agent checks product prices. This is a read-only action, so the result is **Allow**, Rule 4." |
| 0:35–0:45 | **Test 2:** change Agent ID to `AGT-999`, *Place an order*, ₹2,000 → Send | "Test 2. An unknown agent tries to place an order. The result is **Block**, Rule 1." |
| 0:45–0:58 | **Test 3:** AGT-001, *Place an order*, Smartphone ₹10,000 → Send | "Test 3. A registered agent wants to buy a ten thousand rupee phone. This is above the limit, so the result is **Ask Customer**, Rule 6." |
| 0:58–1:08 | **Test 4:** AGT-001, *Place an order*, Wireless Earbuds ₹2,000 → Send | "Test 4. The same agent buys a two thousand rupee product. It is within the limit, so **Allow**, Rule 5." |
| 1:08–1:18 | **Test 5:** `AGT-002`, *Place an order*, ₹2,000 → Send | "Test 5. This agent was revoked by the customer. Even a small order is **Block**, Rule 2." |
| 1:18–1:28 | **Test 6:** AGT-001, *Request a refund*, Smart Watch ₹8,000 → Send | "Test 6. A refund of eight thousand rupees is also above the limit, so **Ask Customer**." |
| 1:28–1:40 | Customer Confirmation page → click **Confirm** on one request | "On the Customer Confirmation page the customer can confirm or reject. The transaction is allowed only after the confirmation is recorded, and the engine checks the rules again." |
| 1:40–1:50 | Audit Log page → Security Summary page | "Every request is saved in the audit log, which I can download as CSV. The security summary shows how many requests were allowed, blocked, and sent to the customer. Thank you." |

## Tips

- Keep the browser zoom at 100% so the text is readable.
- If you make a mistake, click **Reset demo data** and record again.
- Keep the video under 2 minutes. A short video also keeps the ZIP under 35 MB. If the video file is large, upload it as an *unlisted* YouTube video or a Google Drive link ("anyone with the link can view"), and save the link in `video/video_link.txt`.

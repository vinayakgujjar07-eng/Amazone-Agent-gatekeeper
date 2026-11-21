# Submission guide: GitHub, screenshots, video and ZIP

## Part 1: GitHub (minimum 5 commits on at least 3 different days)

**The rule:** your commit history must be **real**. Git records the real date of each commit. Do **not** change dates
(never use `--date`, never edit the system clock, never rewrite history). To meet the "three different days" rule, start now
and make genuine commits on three separate calendar days. Check the submission deadline today. If there are fewer than three days left, tell your
teacher honestly instead of faking the history.

### One-time setup

1. Create a free account at https://github.com .
2. Install **Git for Windows** from https://git-scm.com/download/win (accept the default options).
3. Open Command Prompt and set your identity (once):
   ```
   git config --global user.name "Your Name"
   git config --global user.email "your-github-email@example.com"
   ```

### Create the repository

1. On github.com click **+ → New repository**.
2. Repository name: `AgentGate`. Choose **Public** (or Private and add your teacher as a collaborator, if your teacher asks for that).
3. Do **not** tick "Add a README" (you already have one). Click **Create repository**.
4. Copy the repository address, for example `https://github.com/YOUR-NAME/AgentGate.git`.

### First upload (Day 1) – open Command Prompt inside the AgentGate folder

```
git init
git branch -M main
git remote add origin https://github.com/YOUR-NAME/AgentGate.git
git add decision_engine.py tests test_cases.py
git commit -m "Add decision engine with 8 security rules and test cases"
git push -u origin main
```
(The first `git push` opens a browser window to sign in to GitHub.)

### Suggested commit plan (use your own real working days)

| Commit | When | What to add (`git add ...`) | Example message |
|---|---|---|---|
| 1 | Day 1 | `decision_engine.py test_cases.py tests` | Add decision engine with 8 security rules and test cases |
| 2 | Day 1 | `agent_manager.py audit_logger.py pending_manager.py data requirements.txt .gitignore` | Add agent manager, audit logger and demo data |
| 3 | Day 2 | `app.py` | Add Streamlit app with dashboard, simulator and confirmation |
| 4 | Day 2 | `README.md` | Add README with Windows run instructions |
| 5 | Day 3 | **Your own modification** (see PROMPTS.md, section C) | Describe what you really changed |
| 6 | Day 3 | `PROMPTS.md report screenshots video SUBMISSION_GUIDE.md make_zip.py` | Add report, prompts, screenshots and video script |

Before each commit, **run the app or the tests** and read the files you are committing, so that each commit is something you have really reviewed.
For every commit:
```
git status
git add <files>
git commit -m "your message"
git push
```
Add more commits when you really make more changes. Small, honest commits are better than one big upload.

### Share the link

Open your repository in the browser and copy the address from the address bar (for example `https://github.com/YOUR-NAME/AgentGate`).
Open it in a private/incognito window to confirm that your teacher can see it. Then put it in the report:
```
python report/build_report.py --github https://github.com/YOUR-NAME/AgentGate --enrollment YOUR-NUMBER
```

---

## Part 2: Screenshots (you must capture these yourself)

Press `Windows + Shift + S` to capture, or use the Snipping Tool. Save PNG files in the `screenshots` folder with these names.
Start with **Reset demo data** so that the screens are clean.

| # | File name | How to get it |
|---|---|---|
| 1 | `01_dashboard.png` | **A. Dashboard** page (best after you have sent a few requests, so the counts are not zero) |
| 2 | `02_agent_registration.png` | **B. Agent Registration**: register a new agent, e.g. customer "Test Customer", then capture the page showing the success message and the agent table |
| 3 | `03_agent_revocation.png` | **C. Agent Revocation**: revoke an agent and capture the success message with the revoked date and time |
| 4 | `04_decision_allow.png` | **D. Simulator**: AGT-001, Place an order, Wireless Earbuds ₹2,000 → green ALLOW card |
| 5 | `05_decision_block.png` | **D. Simulator**: AGT-999 (unknown) or AGT-002 (revoked), Place an order → red BLOCK card |
| 6 | `06_decision_ask_customer.png` | **D. Simulator**: AGT-001, Place an order, Smartphone ₹10,000 → yellow ASK CUSTOMER card (you can also capture the Customer Confirmation page) |
| 7 | `07_audit_log.png` | **G. Audit Log** page showing several rows and the download button |
| 8 | `08_testing_results.png` | **Testing Results** page after clicking *Run the six test cases* (and/or the Command Prompt output of `python tests/test_gatekeeper.py`) |

Check that every screenshot is clear, readable and not cropped.

## Part 3: Video

Use `video/video_script.md`. Record it yourself and speak in your own voice (1–2 minutes). Save the file in `video/`
(for example `video/demo.mp4`), or save an unlisted link in `video/video_link.txt` if the file is large.

## Part 4: Final ZIP (maximum 35 MB)

1. Make sure these exist: `report/Report.pdf` (with your GitHub link and enrollment number), `PROMPTS.md` (with your own contribution filled in),
   8 screenshots, and the video or the video link.
2. In Command Prompt inside the AgentGate folder run:
   ```
   python make_zip.py
   ```
3. This creates `AgentGate.zip` **next to** the AgentGate folder. It contains `Report.pdf`, `PROMPTS.md` and the complete `AgentGate/` project folder.
   The script prints a warning if something is missing and shows the file size.
4. Open the ZIP once to check it. Upload `AgentGate.zip` as your teacher instructed.

## Final checklist

- [ ] App runs with `streamlit run app.py`
- [ ] `python tests/test_gatekeeper.py` shows 6 of 6 required tests passed
- [ ] GitHub repository is public (or shared) with at least 5 real commits on at least 3 different days
- [ ] GitHub link and enrollment number are in `Report.pdf` (still 2 pages)
- [ ] `PROMPTS.md` "My Own Contribution" is filled in honestly
- [ ] 8 screenshots in `screenshots/`
- [ ] Video recorded by you (or link in `video/video_link.txt`)
- [ ] `AgentGate.zip` is under 35 MB

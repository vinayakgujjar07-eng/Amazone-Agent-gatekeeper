"""
make_zip.py
===========
Builds the final submission file  AgentGate.zip  (saved NEXT TO the AgentGate folder).

Run from inside the AgentGate folder:
    python make_zip.py

The ZIP contains:
    Report.pdf              (copy of report/Report.pdf, for easy marking)
    PROMPTS.md              (copy of PROMPTS.md)
    AgentGate/              (the complete project folder, including screenshots/ and video/)

The script also checks the assignment limits (35 MB, report present, screenshots present).
"""

import os
import zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(ROOT)
ZIP_PATH = os.path.join(PARENT, "AgentGate.zip")
MAX_MB = 35

SKIP_DIRS = {"__pycache__", "venv", ".venv", ".git", ".idea", ".vscode"}
SKIP_FILES = {"pending_requests.json", ".DS_Store"}
IMAGE_EXT = (".png", ".jpg", ".jpeg")


def main():
    report = os.path.join(ROOT, "report", "Report.pdf")
    prompts = os.path.join(ROOT, "PROMPTS.md")

    problems = []
    if not os.path.exists(report):
        problems.append("report/Report.pdf is missing.")
    if not os.path.exists(prompts):
        problems.append("PROMPTS.md is missing.")

    shots = [f for f in os.listdir(os.path.join(ROOT, "screenshots")) if f.lower().endswith(IMAGE_EXT)]
    if len(shots) < 8:
        problems.append("screenshots/ has {} image(s). The assignment needs 8.".format(len(shots)))

    video_files = [f for f in os.listdir(os.path.join(ROOT, "video")) if f != ".gitkeep"]
    if not video_files:
        problems.append("video/ is empty. Add your video file or a text file with the video link.")

    if problems:
        print("WARNING - please fix these before submitting:")
        for p in problems:
            print("  - " + p)
        print()

    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as z:
        if os.path.exists(report):
            z.write(report, "Report.pdf")
        if os.path.exists(prompts):
            z.write(prompts, "PROMPTS.md")
        for folder, dirs, files in os.walk(ROOT):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for name in files:
                if name in SKIP_FILES or name.endswith(".pyc"):
                    continue
                full = os.path.join(folder, name)
                z.write(full, os.path.join("AgentGate", os.path.relpath(full, ROOT)))

    size_mb = os.path.getsize(ZIP_PATH) / (1024 * 1024)
    print("Created: {}".format(ZIP_PATH))
    print("Size: {:.2f} MB (limit {} MB)".format(size_mb, MAX_MB))
    if size_mb > MAX_MB:
        print("TOO BIG: upload the video to Google Drive/YouTube (unlisted), put the link in "
              "video/video_link.txt, delete the video file, and run this script again.")
    else:
        print("Size is OK.")


if __name__ == "__main__":
    main()

# AI Resume Screener & Skill-Gap Analyzer

A beginner-friendly Python project that compares a resume against a job
description and reports:
- An overall match score
- A text-similarity score (TF-IDF + cosine similarity)
- Which required skills are present, and which are missing

Built for VS Code. No paid tools, no API keys, works fully offline once
set up.

---

## 1. How the project is organized

```
resume-screener/
├── app.py                        <- Streamlit web app (the UI you'll actually use)
├── requirements.txt               <- list of packages to install
├── .gitignore
├── README.md                      <- this file
├── data/
│   ├── sample_resume.txt          <- test resume (already included)
│   └── sample_job_description.txt <- test job post (already included)
└── src/
    ├── __init__.py
    ├── skills_list.py             <- dictionary of ~90 tech/soft skills
    ├── parser.py                  <- Stage 1: file -> plain text
    ├── matcher.py                 <- Stage 2: text -> cleaned text + skills found
    └── scorer.py                  <- Stage 3: resume + JD -> final score report
```

**The pipeline, in one sentence:** a file goes into `parser.py`, comes out
as plain text, that text goes into `matcher.py` to find skills, and
`scorer.py` combines everything into one final report that `app.py` displays.

---

## 2. Setting up in VS Code (do this once)

### Step 1 — Install VS Code + extensions
1. Download VS Code: https://code.visualstudio.com
2. Open VS Code → click the Extensions icon on the left sidebar (or press `Ctrl+Shift+X`)
3. Install: **Python** (by Microsoft) and **Pylance**

### Step 2 — Open the project folder
1. Extract/copy this `resume-screener` folder anywhere on your computer
2. In VS Code: `File > Open Folder...` → select the `resume-screener` folder

### Step 3 — Create a virtual environment
A virtual environment keeps this project's packages separate from everything
else on your computer.

Open the built-in terminal: `Ctrl + \`` (backtick), then run:

```bash
python -m venv venv
```

Activate it:
- **Windows (PowerShell):** `venv\Scripts\Activate.ps1`
- **Windows (cmd.exe):** `venv\Scripts\activate.bat`
- **Mac / Linux:** `source venv/bin/activate`

You'll know it worked because your terminal prompt will now start with `(venv)`.

VS Code may also pop up a message asking "Select Python Interpreter" — click
it and choose the one inside `venv`. If it doesn't ask, press `Ctrl+Shift+P`,
type "Python: Select Interpreter", and pick the `venv` one.

### Step 4 — Install the packages
With `(venv)` active in the terminal:

```bash
pip install -r requirements.txt
```

This installs everything the project needs: PyPDF2, python-docx,
scikit-learn, nltk, and streamlit.

---

## 3. Running it — 3 ways, from simplest to full app

### A) Test Stage 1 alone (file → text)
```bash
python src/parser.py data/sample_resume.txt
```
This should print the resume's raw text at the bottom of your terminal.

### B) Test Stage 2 alone (text → skills found)
```bash
python src/matcher.py data/sample_resume.txt
```
This should print a list of ~26 detected skills like `python`, `sql`, `tensorflow`.

### C) Test Stage 3 — the full report (resume + job description → score)
```bash
python src/scorer.py data/sample_resume.txt data/sample_job_description.txt
```
Expected output (using the included sample files):
```
===== RESUME MATCH REPORT =====
Overall Score:        64.74%
Text Similarity:      34.36%
Skill Match:          85.0%
Matched Skills:       [...]
Missing Skills:       ['azure', 'data science', 'kubernetes']
```

### D) Run the actual web app (what you'll show people / use for real)
```bash
streamlit run app.py
```
This opens a browser tab (usually `http://localhost:8501`) where you can
upload a real resume file and paste a real job description, then click
**Analyze Match**.

To stop the app, go back to the terminal and press `Ctrl + C`.

---

## 4. Using it with your OWN resume

1. Have your resume as a `.pdf`, `.docx`, or `.txt` file
2. Run `streamlit run app.py`
3. Upload your resume file in the "1. Resume" section
4. Copy-paste any real job posting's text into the "2. Job Description" box
5. Click **Analyze Match**

You can also drop your own resume into the `data/` folder and run it from
the command line instead of the web app, e.g.:
```bash
python src/scorer.py data/my_resume.pdf data/some_job.txt
```

---

## 5. How the matching actually works (for when someone asks you in an interview)

- **Text similarity**: both documents are converted into TF-IDF vectors
  (a way of representing text as numbers weighted by how distinctive each
  word is), then compared using cosine similarity — a standard measure of
  how "close" two pieces of text are in meaning-space. Score range: 0–100%.
- **Skill match**: both documents are scanned against a curated list of
  ~90 tech/soft skills (`src/skills_list.py`). We check which skills the
  job description mentions, then see how many of those the resume also
  has. Score = (skills in both) ÷ (skills the JD asked for).
- **Overall score**: a weighted blend — 40% text similarity, 60% skill
  match (skills matter more than general wording for this use case). You
  can change these weights in `src/scorer.py` → `generate_report()`.

---

## 6. Ideas to extend it later (once you're comfortable)

- Add more skills to `src/skills_list.py` for your target field
- Replace TF-IDF with `sentence-transformers` embeddings for smarter
  semantic matching (understands "ML" ≈ "machine learning" automatically)
- Add a bar chart of matched vs. missing skills (Streamlit has built-in charting)
- Let it accept multiple resumes at once and rank them for a given job
- Save each analysis result to a CSV file so you can track applications over time

---

## 7. Common problems

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'streamlit'` | You forgot to activate the venv, or forgot `pip install -r requirements.txt` |
| `streamlit: command not found` | Same as above — activate venv first |
| PDF text comes out empty or garbled | The PDF is likely a scanned image, not real text. PyPDF2 can't read images — you'd need OCR (a more advanced topic) |
| VS Code still uses the wrong Python | `Ctrl+Shift+P` → "Python: Select Interpreter" → choose the one inside `venv/` |

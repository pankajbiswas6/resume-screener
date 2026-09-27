"""
app.py
------
This is the front door of the project. It's a small web page (built with
Streamlit) where you can:
  1. Upload a resume (PDF / DOCX / TXT)
  2. Paste or upload a job description
  3. Click a button and see the match score + skill breakdown

Run it with:
    streamlit run app.py

This does NOT contain any new logic — it just imports the three pipeline
stages you already tested from the command line, and displays their
output nicely.
"""

import os
import tempfile
import streamlit as st

from src.parser import extract_text
from src.scorer import generate_report

st.set_page_config(page_title="AI Resume Screener", page_icon="🧾", layout="centered")

st.title("🧾 AI Resume Screener")
st.write(
    "Upload a resume and paste a job description. "
    "This tool scores how well they match using TF-IDF text similarity "
    "and a skill-keyword comparison."
)

# ---------- Step 1: get the resume ----------
st.header("1. Resume")
resume_file = st.file_uploader("Upload resume (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"])

resume_text = ""
if resume_file is not None:
    # Streamlit gives us the file in memory; our parser functions expect a
    # file PATH, so we save it to a temporary file first.
    suffix = os.path.splitext(resume_file.name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(resume_file.getbuffer())
        tmp_path = tmp.name

    try:
        resume_text = extract_text(tmp_path)
        st.success(f"Resume loaded ({len(resume_text)} characters extracted).")
        with st.expander("Preview extracted resume text"):
            st.text(resume_text[:1500] + ("..." if len(resume_text) > 1500 else ""))
    except Exception as e:
        st.error(f"Could not read resume: {e}")
    finally:
        os.remove(tmp_path)  # clean up the temp file

# ---------- Step 2: get the job description ----------
st.header("2. Job Description")
jd_text = st.text_area(
    "Paste the job description here",
    height=200,
    placeholder="Paste the full job description text...",
)

# ---------- Step 3: run the analysis ----------
st.header("3. Results")

if st.button("Analyze Match", type="primary"):
    if not resume_text:
        st.warning("Please upload a resume first.")
    elif not jd_text.strip():
        st.warning("Please paste a job description first.")
    else:
        report = generate_report(resume_text, jd_text)

        col1, col2, col3 = st.columns(3)
        col1.metric("Overall Score", f"{report['overall_score']}%")
        col2.metric("Text Similarity", f"{report['text_similarity']}%")
        col3.metric("Skill Match", f"{report['skill_match_percent']}%")

        st.subheader("✅ Matched Skills")
        if report["matched_skills"]:
            st.write(", ".join(report["matched_skills"]))
        else:
            st.write("No matching skills found.")

        st.subheader("❌ Missing Skills")
        if report["missing_skills"]:
            st.write(", ".join(report["missing_skills"]))
            st.caption("Consider highlighting these if you actually have them, or upskilling in these areas.")
        else:
            st.write("None — the resume covers every skill detected in the job description!")

st.divider()
st.caption(
    "How it works: resumes/JDs are parsed to plain text, cleaned, compared with "
    "TF-IDF + cosine similarity for overall topic similarity, and separately scanned "
    "against a skill dictionary for a skill-level match."
)

"""
scorer.py
---------
Job: compare a resume against a job description and produce:
  1. an overall similarity score (0-100%) using TF-IDF + cosine similarity
  2. a skill match breakdown (which required skills the resume has / lacks)

This is the THIRD and FINAL stage of the pipeline:
   resume text + job description text  --->  scorer.py  --->  final report

WHAT IS "TF-IDF + COSINE SIMILARITY" IN PLAIN ENGLISH?
- TF-IDF turns each document (resume, job description) into a list of
  numbers representing how important each word is to that document.
- Cosine similarity then measures the "angle" between those two number
  lists. 1.0 = the documents talk about identical things. 0.0 = completely
  unrelated. This is a well-known, standard, explainable technique used in
  real search engines and recommendation systems — good to mention in an
  interview.

Run this file directly to test it on the sample data included:
    python src/scorer.py
"""

import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

try:
    from matcher import clean_text, extract_skills
    from parser import extract_text
except ImportError:
    from src.matcher import clean_text, extract_skills
    from src.parser import extract_text


def compute_text_similarity(resume_text: str, jd_text: str) -> float:
    """
    Returns a similarity score between 0 and 100 (percentage).
    """
    resume_clean = clean_text(resume_text)
    jd_clean = clean_text(jd_text)

    # TfidfVectorizer needs a LIST of documents, so we pass both as a list of 2
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform([resume_clean, jd_clean])

    # cosine_similarity returns a 2x2 matrix; [0][1] is the score we want
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

    return round(similarity * 100, 2)


def compute_skill_match(resume_text: str, jd_text: str) -> dict:
    """
    Finds which skills the job description asks for, and how many of
    those the resume actually has.
    Returns a dict with matched skills, missing skills, and a percentage.
    """
    resume_skills = set(extract_skills(resume_text))
    jd_skills = set(extract_skills(jd_text))

    if not jd_skills:
        # Job description didn't mention any skills from our list
        return {
            "matched": [],
            "missing": [],
            "match_percent": 0.0,
            "jd_skills_found": [],
        }

    matched = sorted(resume_skills & jd_skills)   # skills in BOTH
    missing = sorted(jd_skills - resume_skills)   # skills in JD but NOT resume

    match_percent = round(len(matched) / len(jd_skills) * 100, 2)

    return {
        "matched": matched,
        "missing": missing,
        "match_percent": match_percent,
        "jd_skills_found": sorted(jd_skills),
    }


def generate_report(resume_text: str, jd_text: str) -> dict:
    """
    Combines text similarity + skill match into one final report.
    This is the function app.py (the Streamlit UI) will call.
    """
    text_score = compute_text_similarity(resume_text, jd_text)
    skill_result = compute_skill_match(resume_text, jd_text)

    # Simple weighted combination: 40% overall text similarity,
    # 60% how many required skills actually matched.
    # (Feel free to change these weights once you understand the pipeline.)
    overall_score = round(0.4 * text_score + 0.6 * skill_result["match_percent"], 2)

    return {
        "overall_score": overall_score,
        "text_similarity": text_score,
        "skill_match_percent": skill_result["match_percent"],
        "matched_skills": skill_result["matched"],
        "missing_skills": skill_result["missing"],
    }


# ---- Test block: runs only when this file is executed directly ----
if __name__ == "__main__":
    resume_path = sys.argv[1] if len(sys.argv) > 1 else "data/sample_resume.txt"
    jd_path = sys.argv[2] if len(sys.argv) > 2 else "data/sample_job_description.txt"

    resume_text = extract_text(resume_path)
    jd_text = extract_text(jd_path)

    report = generate_report(resume_text, jd_text)

    print("===== RESUME MATCH REPORT =====")
    print(f"Overall Score:        {report['overall_score']}%")
    print(f"Text Similarity:      {report['text_similarity']}%")
    print(f"Skill Match:          {report['skill_match_percent']}%")
    print(f"Matched Skills:       {report['matched_skills']}")
    print(f"Missing Skills:       {report['missing_skills']}")

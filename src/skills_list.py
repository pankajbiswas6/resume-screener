"""
skills_list.py
---------------
This file just holds a big Python list of common tech/soft skills.

WHY A PLAIN LIST INSTEAD OF AN AI MODEL?
Detecting "skills" with 100% accuracy normally needs a trained NLP model.
For a first version, a keyword list is simpler, faster, needs no downloads,
and is very easy to explain in an interview: "I match resume text against
a curated skill dictionary using simple string search."

You can freely add/remove skills from this list later.
"""

SKILLS = [
    # Programming languages
    "python", "java", "c++", "c", "javascript", "typescript", "sql", "r",
    "go", "rust", "kotlin", "swift", "php", "scala",

    # ML / Data Science
    "machine learning", "deep learning", "data science", "nlp",
    "natural language processing", "computer vision", "tensorflow",
    "pytorch", "scikit-learn", "keras", "pandas", "numpy", "matplotlib",
    "opencv", "nltk", "spacy", "hugging face", "transformers",
    "data analysis", "data visualization", "statistics", "regression",
    "classification", "clustering", "neural networks",

    # Web / Backend
    "flask", "django", "fastapi", "react", "node.js", "express",
    "rest api", "html", "css", "bootstrap",

    # Databases
    "mysql", "postgresql", "mongodb", "sqlite", "oracle",

    # Cloud / DevOps
    "aws", "azure", "gcp", "google cloud", "docker", "kubernetes",
    "git", "github", "linux", "ci/cd", "jenkins",

    # Soft skills (often screened for too)
    "communication", "teamwork", "leadership", "problem solving",
    "project management", "time management", "critical thinking",
]

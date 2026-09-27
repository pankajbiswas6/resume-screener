"""
matcher.py
----------
Job: take raw text (from parser.py) and figure out:
  1. a "cleaned" version of it (lowercase, no extra symbols)
  2. which skills (from skills_list.py) actually appear in it

This is the SECOND stage of the pipeline:
   plain text  --->  matcher.py  --->  cleaned text + list of skills found

Run this file directly to test it on its own:
    python src/matcher.py data/sample_resume.txt
"""

import sys
import re

# Handle being run both as "python src/matcher.py" (script) and
# imported as "from src.matcher import ..." (module) — this try/except
# lets both work without you needing to worry about it.
try:
    from skills_list import SKILLS
    from parser import extract_text
except ImportError:
    from src.skills_list import SKILLS
    from src.parser import extract_text


def clean_text(text: str) -> str:
    """
    Lowercases text and collapses multiple spaces/newlines into one space.
    Keeps letters, numbers, spaces, '+', '#', '.' (so "c++", "c#", "node.js"
    survive cleaning instead of becoming "c" or "nodejs").
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#. ]", " ", text)   # remove weird symbols
    text = re.sub(r"\s+", " ", text)             # collapse whitespace
    return text.strip()


def extract_skills(text: str, skill_list=SKILLS) -> list:
    """
    Checks which skills from skill_list appear inside the cleaned text.
    Uses word-boundary matching so "r" doesn't match inside "programming".

    IMPORTANT DETAIL: short skills can accidentally sit inside longer ones
    (e.g. "c" is technically a valid word-boundary match inside "c++").
    To avoid that, we build ONE combined pattern with the LONGEST skill
    names first, so "c++" gets matched (and "used up") before "c" ever
    gets a chance to match on its own.

    Returns a sorted list of the skills that were found.
    """
    cleaned = clean_text(text)

    # Map "cleaned version of skill" -> "original skill name" so we can
    # report skills back in their original, readable form.
    cleaned_to_original = {clean_text(skill): skill for skill in skill_list}

    # Longest skill text first = matched first = "uses up" that text
    # before a shorter skill can incorrectly match inside it.
    sorted_clean_skills = sorted(cleaned_to_original.keys(), key=len, reverse=True)

    # NOTE: we deliberately do NOT use \b here. \b is defined as a
    # transition between a "word" character and a "non-word" character.
    # Skills like "c++" END in "+", which is itself a non-word character,
    # so \b fails right after it (no transition from non-word to non-word).
    # Instead we require: not preceded/followed by a letter or digit —
    # this correctly treats "+", "#", "." as valid skill-boundary characters.
    combined_pattern = (
        r"(?<![a-z0-9])(" + "|".join(re.escape(s) for s in sorted_clean_skills) + r")(?![a-z0-9])"
    )
    matches = re.findall(combined_pattern, cleaned)

    found_original = {cleaned_to_original[m] for m in matches}
    return sorted(found_original)


# ---- Test block: runs only when this file is executed directly ----
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python src/matcher.py <path_to_file>")
        sys.exit(1)

    raw_text = extract_text(sys.argv[1])
    skills_found = extract_skills(raw_text)

    print(f"Skills found ({len(skills_found)}):")
    for s in skills_found:
        print(f"  - {s}")

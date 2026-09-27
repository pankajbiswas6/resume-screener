"""
parser.py
---------
Job: take a resume file (PDF, DOCX, or TXT) and return its plain text.

This is the FIRST stage of the pipeline:
   file on disk  --->  parser.py  --->  plain text string

Run this file directly to test it on its own:
    python src/parser.py data/sample_resume.txt
"""

import sys
import os

# PyPDF2 reads .pdf files
from PyPDF2 import PdfReader

# python-docx reads .docx files (note: import name is "docx", not "python-docx")
from docx import Document


def extract_text_from_pdf(file_path: str) -> str:
    """Reads a PDF file and returns all its text as one string."""
    reader = PdfReader(file_path)
    text_parts = []
    for page in reader.pages:
        page_text = page.extract_text() or ""  # extract_text() can return None
        text_parts.append(page_text)
    return "\n".join(text_parts)


def extract_text_from_docx(file_path: str) -> str:
    """Reads a Word (.docx) file and returns all its text as one string."""
    document = Document(file_path)
    paragraphs = [para.text for para in document.paragraphs]
    return "\n".join(paragraphs)


def extract_text_from_txt(file_path: str) -> str:
    """Reads a plain .txt file. Useful for quick testing without real resumes."""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def extract_text(file_path: str) -> str:
    """
    Main entry point: looks at the file extension and calls the right
    function above. This is the only function other files need to import.
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    elif ext == ".txt":
        return extract_text_from_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}. Use .pdf, .docx, or .txt")


# ---- This block only runs when you execute this file directly ----
# (it does NOT run when another file imports functions from parser.py)
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python src/parser.py <path_to_file>")
        sys.exit(1)

    path = sys.argv[1]
    text = extract_text(path)
    print("----- EXTRACTED TEXT -----")
    print(text)
    print("---------------------------")
    print(f"Total characters extracted: {len(text)}")

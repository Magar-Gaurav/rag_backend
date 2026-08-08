from pathlib import Path

import fitz


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file."""

    document = fitz.open(file_path)

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text


def extract_text_from_txt(file_path: str) -> str:
    """Extract text from a TXT file."""

    return Path(file_path).read_text(encoding="utf-8")


def extract_text(file_path: str) -> str:
    """Extract text based on the file extension."""

    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    if extension == ".txt":
        return extract_text_from_txt(file_path)

    raise ValueError("Unsupported file type")
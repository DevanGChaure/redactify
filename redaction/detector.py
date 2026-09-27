import os

from redaction.pdf_redactor import extract_text_from_pdf
from redaction.image_redactor import extract_text_from_image_file


def extract_text(file_path):
    """Dispatch to the right extractor based on file extension."""
    ext = os.path.splitext(file_path)[1].lower().lstrip(".")

    if ext == "pdf":
        return extract_text_from_pdf(file_path)
    elif ext in ("png", "jpg", "jpeg"):
        return extract_text_from_image_file(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
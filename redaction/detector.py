import os

from redaction.pdf_redactor import extract_text_from_pdf
from redaction.image_redactor import extract_text_from_image_file
from redaction.regex_detector import detect_regex_pii
from redaction.ner_detector import detect_ner_pii


def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower().lstrip(".")

    if ext == "pdf":
        return extract_text_from_pdf(file_path)
    elif ext in ("png", "jpg", "jpeg"):
        return extract_text_from_image_file(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def detect_all_pii(text):
    """
    Run both detection layers, then deduplicate overlapping spans
    (prefer regex over NER when they detect the same text) and drop
    low-confidence NER noise.
    """
    regex_detections = detect_regex_pii(text)
    ner_detections = detect_ner_pii(text)

    # Remove NER detections that overlap with a regex detection —
    # regex is more precise for structured PII, so it wins.
    def overlaps(a, b):
        return a["start"] < b["end"] and b["start"] < a["end"]

    filtered_ner = [
        ner for ner in ner_detections
        if not any(overlaps(ner, rx) for rx in regex_detections)
    ]

    # Drop NER detections below a reasonable confidence floor
    # (ORG detections on structured docs are frequently noise)
    filtered_ner = [d for d in filtered_ner if d["confidence"] >= 0.75]

    return regex_detections + filtered_ner
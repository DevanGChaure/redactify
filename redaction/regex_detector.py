import re


PATTERNS = {
    "EMAIL": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
    "PHONE": r"(?<!\d)[6-9]\d{9}(?!\d)",
    "AADHAAR": r"\b\d{4}\s?\d{4}\s?\d{4}\b",
    "PAN": r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
    "IP_ADDRESS": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
}

CONFIDENCE = {
    "EMAIL": 0.99,
    "PHONE": 0.95,
    "AADHAAR": 0.97,
    "PAN": 0.98,
    "IP_ADDRESS": 0.90,
}


def detect_regex_pii(text):
    detections = []
    for pii_type, pattern in PATTERNS.items():
        for match in re.finditer(pattern, text):
            detections.append({
                "text": match.group(),
                "type": pii_type,
                "start": match.start(),
                "end": match.end(),
                "confidence": CONFIDENCE[pii_type],
                "method": "regex",
            })
    return detections

import spacy

_nlp = None


def get_nlp():
    """Lazy-load the spaCy model once, reused across calls."""
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("en_core_web_sm")
    return _nlp


RELEVANT_LABELS = {
    "PERSON": "PERSON",
    "GPE": "LOCATION",
    "ORG": "ORGANIZATION",
    "DATE": "DATE",
}

CONFIDENCE = {
    "PERSON": 0.85,
    "LOCATION": 0.75,
    "ORGANIZATION": 0.70,
    "DATE": 0.65,
}


def detect_ner_pii(text):
    """
    Run spaCy NER over text and return detections for PII-relevant entity types.
    Confidence is lower than regex since NER is probabilistic, not pattern-matched.
    """
    nlp = get_nlp()
    doc = nlp(text)
    detections = []

    for ent in doc.ents:
        if ent.label_ in RELEVANT_LABELS:
            pii_type = RELEVANT_LABELS[ent.label_]
            detections.append({
                "text": ent.text,
                "type": pii_type,
                "start": ent.start_char,
                "end": ent.end_char,
                "confidence": CONFIDENCE[pii_type],
                "method": "ner",
            })

    return detections

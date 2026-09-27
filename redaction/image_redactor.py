from redaction.ocr import extract_text_from_image


def extract_text_from_image_file(image_path):
    """Extract text from a standalone PNG/JPG upload."""
    return extract_text_from_image(image_path)

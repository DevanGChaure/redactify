import pytesseract
from PIL import Image


def extract_text_from_image(image_path):
    """Run OCR on an image file and return extracted text."""
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text


def extract_text_from_pil_image(pil_image):
    """Run OCR directly on an in-memory PIL image (used for rendered PDF pages)."""
    return pytesseract.image_to_string(pil_image)
import fitz  # PyMuPDF
from PIL import Image
import io

from redaction.ocr import extract_text_from_pil_image


def extract_text_from_pdf(pdf_path):
    """
    Try direct text extraction first (fast, works for text-based PDFs).
    If a page has no extractable text, render it as an image and OCR it
    (handles scanned PDFs).
    """
    doc = fitz.open(pdf_path)
    full_text = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text().strip()

        if text:
            full_text.append(text)
        else:
            # No extractable text -> likely scanned. Render page to image and OCR.
            pix = page.get_pixmap(dpi=200)
            img_bytes = pix.tobytes("png")
            pil_image = Image.open(io.BytesIO(img_bytes))
            ocr_text = extract_text_from_pil_image(pil_image)
            full_text.append(ocr_text)

    doc.close()
    return "\n".join(full_text)

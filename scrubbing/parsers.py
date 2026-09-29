import io
import pdfplumber
import docx

from .engine import ShadowScrubEngine

scrubber = ShadowScrubEngine()

def process_pdf_file(file_bytes: bytes) -> tuple[str, dict]:
    """
        Extract text from a PDF, scrub any PII, then returns clean texts and summary.
    """
    raw_text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text and page_text.strip():
                raw_text += page_text + '\n'
    result = scrubber.sanitize(raw_text)
    return result['clean_result'], result['detected_summary']

def process_docx_file(file_byte: bytes) -> tuple[str, dict]:
    """ 
        Executes text from a Docx file, scrub any PII, then return a clean text and summary.
    """
    parts = []
    doc = docx.Document(io.BytesIO(file_byte))
    for paragraph in doc.paragraphs:
        text = paragraph.text
        if text and text.strip():
            parts.append(text)
    raw_text = "\n".join(parts)
    
    result = scrubber.sanitize(raw_text)
    return result['clean_result'], result['detected_summary']
    
    

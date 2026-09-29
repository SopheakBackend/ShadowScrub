from celery import shared_task
from .parsers import process_pdf_file, process_docx_file
from .models import SanitizationLog

@shared_task
def sanitize_file_async(file_bytes: bytes, filename: str):
    """ 
        Celery task executing background document parsing and redaction.
    """
    if filename.endswith('.pdf'):
        clean_text, summary = process_pdf_file(file_bytes)
    elif filename.endswith('.docx'):
        clean_text, summary = process_docx_file(file_bytes)
    else:
        return {"error": "Unsupported file format"}
    
    total_detected = sum(summary.values())
    
    SanitizationLog.objects.create(
        total_detected=total_detected,
        detected_summary = summary
    )
    
    return {
        "status": "completed",
        "filename": filename,
        "clean_text": clean_text,
        "summary": summary,
    }
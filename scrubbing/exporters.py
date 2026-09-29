import io
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch


def export_docx_bytes(text: str) -> bytes:
    doc = Document()
    for line in text.splitlines():
        doc.add_paragraph(line)
    buffer = io.BytesIO()
    doc.save(buffer)
    return buffer.getvalue()


def export_pdf_bytes(text: str) -> bytes:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    x = inch
    y = height - inch
    c.setFont("Helvetica", 11)

    for raw_line in text.splitlines():
        line = raw_line if raw_line.strip() else " "
        # simple wrap for long lines
        while len(line) > 95:
            chunk = line[:95]
            c.drawString(x, y, chunk)
            y -= 14
            line = line[95:]
            if y < inch:
                c.showPage()
                c.setFont("Helvetica", 11)
                y = height - inch
        c.drawString(x, y, line)
        y -= 14
        if y < inch:
            c.showPage()
            c.setFont("Helvetica", 11)
            y = height - inch

    c.save()
    return buffer.getvalue()
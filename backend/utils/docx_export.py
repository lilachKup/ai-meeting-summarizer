import io

from docx import Document


def generate_docx(transcript: str, summary: dict) -> bytes:
    doc = Document()
    doc.add_heading("Meeting Summary", 0)

    doc.add_heading("Summary", level=1)
    doc.add_paragraph(summary.get("summary", ""))

    doc.add_heading("Participants", level=1)
    for p in summary.get("participants", []):
        doc.add_paragraph(p, style="List Bullet")

    doc.add_heading("Decisions", level=1)
    for d in summary.get("decisions", []):
        doc.add_paragraph(d, style="List Bullet")

    doc.add_heading("Action Items", level=1)
    for item in summary.get("action_items", []):
        if isinstance(item, dict):
            text = f"{item.get('task', '')} - {item.get('owner', 'TBD')}"
        else:
            text = str(item)
        doc.add_paragraph(text, style="List Bullet")

    doc.add_heading("Full Transcript", level=1)
    doc.add_paragraph(transcript)

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()
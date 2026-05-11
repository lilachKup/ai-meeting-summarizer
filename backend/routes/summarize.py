import json

import anthropic
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel

from services.claude import summarize_transcript
from utils.docx_export import generate_docx

router = APIRouter()


class TranscriptRequest(BaseModel):
    transcript: str


class DownloadRequest(BaseModel):
    transcript: str
    summary: dict


@router.post("/summarize")
def summarize(request: TranscriptRequest):
    if not request.transcript.strip():
        raise HTTPException(status_code=400, detail="Transcript is empty.")

    try:
        result = summarize_transcript(request.transcript)
    except anthropic.APIError as exc:
        raise HTTPException(status_code=502, detail=f"Claude API error: {exc}") from exc
    except (json.JSONDecodeError, ValueError) as exc:
        raise HTTPException(status_code=500, detail=f"Claude returned unexpected response: {exc}") from exc

    return result


@router.post("/download")
def download(request: DownloadRequest):
    try:
        docx_bytes = generate_docx(request.transcript, request.summary)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to generate Word file: {exc}") from exc

    return Response(
        content=docx_bytes,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": "attachment; filename=meeting_summary.docx"},
    )
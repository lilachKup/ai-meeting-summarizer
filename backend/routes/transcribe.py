import os
import openai
from fastapi import APIRouter, File, HTTPException, UploadFile

from services.whisper import transcribe_audio

router = APIRouter()

ALLOWED_EXTENSIONS = {".mp3", ".wav"}

@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    """Receive an audio file and return its transcript.

    Args:
        file: Uploaded audio file (mp3 or wav).

    Returns:
        JSON with a single key ``transcript`` containing the transcribed text.

    Raises:
        HTTPException 400: If no file content is provided.
        HTTPException 502: If the Whisper API call fails.
    """
    audio_bytes = await file.read()

    if not audio_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    
    extension = os.path.splitext(file.filename)[1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type '{extension}'. Allowed: mp3, wav."
        )
        
    try:
        transcript = transcribe_audio(audio_bytes, file.filename)
    except openai.OpenAIError as exc:
        raise HTTPException(status_code=502, detail=f"Whisper API error: {exc}") from exc

    return {"transcript": transcript}
from fastapi import APIRouter, UploadFile, File
from services.whisper import transcribe_audio

router = APIRouter()

@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    transcript = await transcribe_audio(audio_bytes, file.filename)
    return {"transcript": transcript}
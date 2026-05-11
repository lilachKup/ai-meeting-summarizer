import io
import os

import openai
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def transcribe_audio(audio_bytes: bytes, filename: str) -> str:
    """Transcribe audio bytes using OpenAI Whisper API.

    Args:
        audio_bytes: Raw audio file content.
        filename: Original filename, used by Whisper to detect format.

    Returns:
        Transcribed text string.

    Raises:
        openai.OpenAIError: If the Whisper API call fails.
    """
    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = filename

    response = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
    )
    return response.text
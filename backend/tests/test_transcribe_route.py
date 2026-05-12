"""Integration tests for POST /api/transcribe."""

from unittest.mock import patch

import openai
import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)
PATCH_TARGET = "routes.transcribe.transcribe_audio"
FAKE_TRANSCRIPT = "We discussed the Q3 roadmap."


def _upload(audio=b"fake_audio", filename="meeting.mp3"):
    return client.post(
        "/api/transcribe",
        files={"file": (filename, audio, "audio/mpeg")},
    )


def test_transcribe_success_returns_200():
    with patch(PATCH_TARGET, return_value=FAKE_TRANSCRIPT):
        response = _upload()
    assert response.status_code == 200


def test_transcribe_success_returns_transcript():
    with patch(PATCH_TARGET, return_value=FAKE_TRANSCRIPT):
        response = _upload()
    assert response.json() == {"transcript": FAKE_TRANSCRIPT}


def test_transcribe_accepts_wav():
    with patch(PATCH_TARGET, return_value=FAKE_TRANSCRIPT):
        response = _upload(filename="recording.wav")
    assert response.status_code == 200


def test_transcribe_passes_filename_to_whisper():
    with patch(PATCH_TARGET, return_value=FAKE_TRANSCRIPT) as mock:
        _upload(filename="standup.mp3")
    _, called_filename = mock.call_args.args
    assert called_filename == "standup.mp3"


def test_transcribe_passes_bytes_to_whisper():
    with patch(PATCH_TARGET, return_value=FAKE_TRANSCRIPT) as mock:
        _upload(audio=b"real_audio_bytes")
    called_bytes, _ = mock.call_args.args
    assert called_bytes == b"real_audio_bytes"


def test_transcribe_no_file_returns_422():
    response = client.post("/api/transcribe")
    assert response.status_code == 422


def test_transcribe_empty_file_returns_400():
    response = _upload(audio=b"")
    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()


def test_transcribe_unsupported_format_returns_415():
    response = _upload(filename="meeting.pdf")
    assert response.status_code == 415
    assert "Unsupported" in response.json()["detail"]


def test_transcribe_mp4_not_allowed():
    response = _upload(filename="meeting.mp4")
    assert response.status_code == 415


def test_transcribe_whisper_error_returns_502():
    with patch(PATCH_TARGET, side_effect=openai.OpenAIError("rate limit")):
        response = _upload()
    assert response.status_code == 502
    assert "Whisper API error" in response.json()["detail"]

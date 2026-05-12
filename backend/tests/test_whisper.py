"""Unit tests for services/whisper.py."""

from unittest.mock import MagicMock, patch

import openai
import pytest

from services.whisper import transcribe_audio

FAKE_AUDIO = b"fake_audio_bytes"
FAKE_FILENAME = "meeting.mp3"


def _mock_response(text="Hello world"):
    r = MagicMock()
    r.text = text
    return r


def test_transcribe_returns_text():
    with patch("services.whisper.client.audio.transcriptions.create",
               return_value=_mock_response("We discussed the roadmap.")):
        result = transcribe_audio(FAKE_AUDIO, FAKE_FILENAME)
    assert result == "We discussed the roadmap."


def test_transcribe_returns_empty_string():
    with patch("services.whisper.client.audio.transcriptions.create",
               return_value=_mock_response("")):
        result = transcribe_audio(FAKE_AUDIO, FAKE_FILENAME)
    assert result == ""


def test_transcribe_uses_whisper_1_model():
    with patch("services.whisper.client.audio.transcriptions.create",
               return_value=_mock_response()) as mock_create:
        transcribe_audio(FAKE_AUDIO, FAKE_FILENAME)
    assert mock_create.call_args.kwargs["model"] == "whisper-1"


def test_transcribe_file_has_correct_name():
    with patch("services.whisper.client.audio.transcriptions.create",
               return_value=_mock_response()) as mock_create:
        transcribe_audio(FAKE_AUDIO, FAKE_FILENAME)
    assert mock_create.call_args.kwargs["file"].name == FAKE_FILENAME


def test_transcribe_file_contains_correct_bytes():
    with patch("services.whisper.client.audio.transcriptions.create",
               return_value=_mock_response()) as mock_create:
        transcribe_audio(FAKE_AUDIO, FAKE_FILENAME)
    assert mock_create.call_args.kwargs["file"].read() == FAKE_AUDIO


def test_transcribe_accepts_wav_filename():
    with patch("services.whisper.client.audio.transcriptions.create",
               return_value=_mock_response()) as mock_create:
        transcribe_audio(FAKE_AUDIO, "recording.wav")
    assert mock_create.call_args.kwargs["file"].name == "recording.wav"


def test_transcribe_raises_openai_error():
    with patch("services.whisper.client.audio.transcriptions.create",
               side_effect=openai.OpenAIError("quota exceeded")):
        with pytest.raises(openai.OpenAIError, match="quota exceeded"):
            transcribe_audio(FAKE_AUDIO, FAKE_FILENAME)


def test_transcribe_raises_on_unexpected_error():
    with patch("services.whisper.client.audio.transcriptions.create",
               side_effect=ConnectionError("timeout")):
        with pytest.raises(ConnectionError, match="timeout"):
            transcribe_audio(FAKE_AUDIO, FAKE_FILENAME)

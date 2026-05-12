"""Unit tests for services/claude.py."""

import json
from unittest.mock import MagicMock, patch

import anthropic
import pytest

from services.claude import summarize_transcript

VALID_SUMMARY = {
    "summary": "We discussed the roadmap.",
    "participants": ["Alice", "Bob"],
    "decisions": ["Ship on Friday"],
    "action_items": [{"task": "Write tests", "owner": "Alice", "deadline": "Monday"}]
}


def _mock_message(content: str):
    msg = MagicMock()
    msg.content = [MagicMock(text=content)]
    return msg


# --- Happy path ---

def test_summarize_returns_parsed_dict():
    with patch("services.claude.client.messages.create",
               return_value=_mock_message(json.dumps(VALID_SUMMARY))):
        result = summarize_transcript("We talked about the roadmap.")
    assert result == VALID_SUMMARY


def test_summarize_strips_markdown_fences():
    wrapped = f"```json\n{json.dumps(VALID_SUMMARY)}\n```"
    with patch("services.claude.client.messages.create",
               return_value=_mock_message(wrapped)):
        result = summarize_transcript("Some transcript.")
    assert result["summary"] == VALID_SUMMARY["summary"]


def test_summarize_handles_text_before_json():
    with_prefix = f"Here is the analysis:\n{json.dumps(VALID_SUMMARY)}"
    with patch("services.claude.client.messages.create",
               return_value=_mock_message(with_prefix)):
        result = summarize_transcript("Some transcript.")
    assert result["decisions"] == VALID_SUMMARY["decisions"]


def test_summarize_uses_correct_model():
    from config import CLAUDE_MODEL
    with patch("services.claude.client.messages.create",
               return_value=_mock_message(json.dumps(VALID_SUMMARY))) as mock_create:
        summarize_transcript("Some transcript.")
    assert mock_create.call_args.kwargs["model"] == CLAUDE_MODEL


# --- Validation ---

def test_summarize_raises_on_missing_keys():
    incomplete = {"summary": "short", "participants": []}
    with patch("services.claude.client.messages.create",
               return_value=_mock_message(json.dumps(incomplete))):
        with pytest.raises(ValueError, match="missing keys"):
            summarize_transcript("Some transcript.")


def test_summarize_raises_on_no_json():
    with patch("services.claude.client.messages.create",
               return_value=_mock_message("Sorry, I cannot help.")):
        with pytest.raises(ValueError, match="No JSON object found"):
            summarize_transcript("Some transcript.")


def test_summarize_raises_on_invalid_json():
    with patch("services.claude.client.messages.create",
               return_value=_mock_message("{invalid json")):
        with pytest.raises(Exception):
            summarize_transcript("Some transcript.")


# --- Error propagation ---

def test_summarize_raises_anthropic_error():
    with patch("services.claude.client.messages.create",
               side_effect=anthropic.APIError("rate limit", request=MagicMock(), body=None)):
        with pytest.raises(anthropic.APIError):
            summarize_transcript("Some transcript.")

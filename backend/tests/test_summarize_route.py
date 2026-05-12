"""Integration tests for POST /api/summarize and POST /api/download."""

import json
from unittest.mock import patch

import anthropic
import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)
PATCH_TARGET = "routes.summarize.summarize_transcript"

VALID_SUMMARY = {
    "summary": "The team discussed the roadmap.",
    "participants": ["Alice", "Bob"],
    "decisions": ["Ship on Friday"],
    "action_items": [{"task": "Write tests", "owner": "Alice", "deadline": "Monday"}]
}


def test_summarize_success_returns_200():
    with patch(PATCH_TARGET, return_value=VALID_SUMMARY):
        response = client.post("/api/summarize",
                               json={"transcript": "We talked about the roadmap."})
    assert response.status_code == 200


def test_summarize_success_returns_summary():
    with patch(PATCH_TARGET, return_value=VALID_SUMMARY):
        response = client.post("/api/summarize",
                               json={"transcript": "We talked about the roadmap."})
    assert response.json() == VALID_SUMMARY


def test_summarize_empty_transcript_returns_400():
    response = client.post("/api/summarize", json={"transcript": ""})
    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()


def test_summarize_whitespace_only_returns_400():
    response = client.post("/api/summarize", json={"transcript": "   "})
    assert response.status_code == 400


def test_summarize_missing_body_returns_422():
    response = client.post("/api/summarize")
    assert response.status_code == 422


def test_summarize_claude_api_error_returns_502():
    with patch(PATCH_TARGET,
               side_effect=anthropic.APIError("rate limit", request=None, body=None)):
        response = client.post("/api/summarize",
                               json={"transcript": "Some transcript."})
    assert response.status_code == 502
    assert "Claude API error" in response.json()["detail"]


def test_summarize_invalid_json_response_returns_500():
    with patch(PATCH_TARGET, side_effect=ValueError("No JSON object found")):
        response = client.post("/api/summarize",
                               json={"transcript": "Some transcript."})
    assert response.status_code == 500


def test_download_returns_docx():
    response = client.post("/api/download", json={
        "transcript": "We talked.",
        "summary": VALID_SUMMARY
    })
    assert response.status_code == 200
    assert "wordprocessingml" in response.headers["content-type"]


def test_download_filename_is_meeting_summary():
    response = client.post("/api/download", json={
        "transcript": "We talked.",
        "summary": VALID_SUMMARY
    })
    assert "meeting_summary.docx" in response.headers["content-disposition"]


def test_download_returns_valid_docx_bytes():
    response = client.post("/api/download", json={
        "transcript": "We talked.",
        "summary": VALID_SUMMARY
    })
    assert len(response.content) > 0
    assert response.content[:2] == b'PK'

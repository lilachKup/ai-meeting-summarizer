"""Unit tests for utils/docx_export.py."""

import pytest

from utils.docx_export import _is_rtl, generate_docx

HEBREW_SUMMARY = {
    "summary": "הפגישה עסקה בתכנון הרבעון הבא.",
    "participants": ["יואל", "דנה"],
    "decisions": ["לשחרר את הפיצ'ר ביום שישי"],
    "action_items": [{"task": "לכתוב טסטים", "owner": "יואל", "deadline": "יום שני"}]
}

ENGLISH_SUMMARY = {
    "summary": "The team discussed the Q3 roadmap.",
    "participants": ["Alice", "Bob"],
    "decisions": ["Ship on Friday"],
    "action_items": [{"task": "Write tests", "owner": "Alice", "deadline": "Monday"}]
}

EMPTY_SUMMARY = {
    "summary": "Short meeting.",
    "participants": [],
    "decisions": [],
    "action_items": []
}


# --- _is_rtl ---

def test_is_rtl_hebrew_text():
    assert _is_rtl("שלום עולם זה טקסט עברי") is True


def test_is_rtl_english_text():
    assert _is_rtl("Hello this is English text") is False


def test_is_rtl_empty_string():
    assert _is_rtl("") is False


def test_is_rtl_mixed_mostly_hebrew():
    assert _is_rtl("שלום hello שלום עולם") is True


def test_is_rtl_mixed_mostly_english():
    assert _is_rtl("Hello world this is mostly English שלום") is False


# --- generate_docx ---

def test_generate_docx_returns_bytes():
    result = generate_docx("transcript text", ENGLISH_SUMMARY)
    assert isinstance(result, bytes)


def test_generate_docx_is_valid_docx():
    result = generate_docx("transcript text", ENGLISH_SUMMARY)
    # Valid docx files start with PK (zip header)
    assert result[:2] == b'PK'


def test_generate_docx_hebrew_summary():
    result = generate_docx("טקסט בעברית", HEBREW_SUMMARY)
    assert isinstance(result, bytes)
    assert len(result) > 0


def test_generate_docx_empty_lists():
    result = generate_docx("Short transcript.", EMPTY_SUMMARY)
    assert isinstance(result, bytes)


def test_generate_docx_action_item_as_string():
    """Should not crash if action_items contains plain strings instead of dicts."""
    summary = {**ENGLISH_SUMMARY, "action_items": ["Do something"]}
    result = generate_docx("transcript", summary)
    assert isinstance(result, bytes)


def test_generate_docx_missing_optional_fields():
    """Should handle action items with missing owner or deadline."""
    summary = {
        **ENGLISH_SUMMARY,
        "action_items": [{"task": "Do something"}]
    }
    result = generate_docx("transcript", summary)
    assert isinstance(result, bytes)

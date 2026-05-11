import json
import os
import re

import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are an expert meeting analyst. Given a meeting transcript, extract and return ONLY a JSON object with this exact structure — no markdown, no explanation, just raw JSON:

{
  "summary": "2-3 sentence overview of the meeting",
  "participants": ["Name or Speaker 1", "Name or Speaker 2"],
  "decisions": ["Decision 1", "Decision 2"],
  "action_items": [
    {"task": "What needs to be done", "owner": "Who is responsible (if mentioned)"}
  ]
}

Rules:
- If participant names are not mentioned, return an empty participants list. Do not invent speakers unless the transcript clearly separates speakers.
- Be concise but complete
- Extract ALL action items and decisions, even minor ones
- Return valid JSON only"""


def summarize_transcript(transcript: str) -> dict:
    message = client.messages.create(
        # model="claude-opus-4-5",
        model="claude-haiku-4-5",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": f"Please analyze this meeting transcript:\n\n{transcript}"}
        ]
    )

    raw = message.content[0].text

    # Strip markdown code fences if Claude added them
    cleaned = re.sub(r"```json|```", "", raw).strip()

    # If Claude added text before the JSON, find the first {
    json_start = cleaned.find("{")
    if json_start == -1:
        raise ValueError(f"No JSON object found in Claude response: {cleaned!r}")
    cleaned = cleaned[json_start:]

    parsed = json.loads(cleaned)

    # Validate expected keys are present
    expected_keys = {"summary", "participants", "decisions", "action_items"}
    missing = expected_keys - parsed.keys()
    if missing:
        raise ValueError(f"Claude response missing keys: {missing}")

    return parsed
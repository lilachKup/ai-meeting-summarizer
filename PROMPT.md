# System Prompt — Meeting Summarizer

## The Full Prompt
```
You are an expert meeting analyst. Given a meeting transcript, extract and return ONLY a JSON object with this exact structure - no markdown, no explanation, just raw JSON:

{
  "summary": "3-5 sentence overview covering the main topics, context, and outcome of the meeting",
  "participants": ["Name or Speaker 1", "Name or Speaker 2"],
  "decisions": ["Decision 1", "Decision 2"],
  "action_items": [
    {
      "task": "What needs to be done",
      "owner": "Who is responsible, if clearly mentioned",
      "deadline": "Deadline, if clearly mentioned"
    }
  ]
}

Rules:
- Return the JSON keys exactly as shown, in English.
- Return all text values in the same language as the transcript.
- If the transcript is in Hebrew, write the summary, decisions, participants, tasks, owners, and deadlines in Hebrew.
- If participant names are not clearly mentioned, return an empty participants list.
- Do not invent speakers unless the transcript clearly separates speakers.
- For action item owner, use the owner only if clearly mentioned.
- If an action item has no clear owner, write "לא צוין" for Hebrew transcripts or "Not specified" for English transcripts.
- If an action item has no clear deadline, write "לא צוין" for Hebrew transcripts or "Not specified" for English transcripts.
- Be concise but complete.
- Extract all action items and decisions, even minor ones.
- If the transcript is very short or unclear, always return a best-effort summary. For participants, decisions, and action_items return empty arrays if nothing is clear.
- Return valid JSON only.   
```


---

## Why I Built It This Way

**1. Role definition first**
Starting with "You are an expert meeting analyst" sets the context immediately.
The model focuses on structured extraction, not conversation or explanation.

**2. Exact JSON schema in the prompt**
Providing the full schema removes all ambiguity — the model knows exactly what
keys to return, what types they are, and what the values should look like.
This is more reliable than describing the structure in words.

**3. "No markdown, no explanation, just raw JSON"**
Without this instruction, Claude sometimes wraps the response in code fences
(` ```json ``` `) or adds an introductory sentence before the JSON, both of which
break `json.loads()`. Even with this instruction I added defensive parsing in the
code as a safety net.

**4. Language rule — keys in English, values in transcript language**
JSON keys stay in English for reliable parsing regardless of input language.
Values are written in the transcript's language so Hebrew meetings return Hebrew
output without any extra translation step. This was an explicit design decision
to support the mixed Hebrew/English use case.

**5. Explicit fallback rules for missing data**
Telling the model exactly what to return when data is missing:
- Empty list `[]` for participants — because it's an array, an empty list is
  cleaner than a placeholder string
- "לא צוין" / "Not specified" for owner and deadline — because they are strings
  and cannot be empty without breaking the UI display

This prevents null values and inconsistent output across different transcripts.

**6. Best-effort for short or unclear transcripts**
Added a rule to always return a summary even if the transcript is poor quality.
This prevents the entire response from failing just because the audio was unclear.

**7. "Even minor ones" for action items and decisions**
Without this, models tend to filter out small decisions or informal tasks.
This instruction ensures completeness even for casual meetings.
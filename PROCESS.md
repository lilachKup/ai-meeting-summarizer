# PROCESS.md

## System Design — Before Starting

Before writing any code, I consulted both Claude and ChatGPT to validate my approach and tool choices, then did a quick Google search to confirm they were industry-standard.

**Architecture decision:**
- Python (FastAPI) backend — simple, fast to build, good async support
- React frontend — component-based, easy to manage state
- OpenAI Whisper API — best transcription quality for Hebrew/English mixed audio
- Anthropic Claude API — strong instruction-following for structured JSON output

**Plan:**
Build and manually test the backend first, function by function. Once each endpoint worked, move to the frontend. Avoided writing tests upfront due to time constraints — prioritized a working demo, with the option to add tests at the end.

---

## How I Used AI During Development

I used **Claude** as my primary coding assistant for writing and reviewing code,
and **ChatGPT** for understanding specific concepts and validating decisions
(e.g. researching Whisper API options, understanding async vs sync tradeoffs).
I also used Google search and ChatGPT to validate architectural decisions and
cross-check things Claude suggested.

I didn't copy-paste blindly — I read each piece of code, questioned decisions
I wasn't sure about, and added things Claude initially missed like error handling
(400 for empty files, 415 for wrong file type, 502 for API failures).

**Examples of prompts I used:**

- *"Build a FastAPI backend with two routes: one that receives an audio file and
  transcribes it using Whisper, and one that takes a transcript and returns a
  structured summary using Claude API."*

- *"The summarize function can fail if Claude returns markdown instead of raw JSON.
  Add defensive parsing that strips code fences and finds the first { in the response."*

- *"Rewrite whisper.py to follow Python standards — async def was wrong because
  there's no await inside, and import io should be at the top of the file."*

- *"Add RTL support to the Word export — if the transcript is Hebrew, paragraphs
  should be right-aligned."*

---

## Where I Got Stuck and How I Solved It

**1. Choosing the right Whisper API**
Not familiar with Whisper options upfront. Researched the difference between
running Whisper locally vs using the OpenAI API, and chose the API for simplicity
and reliability within the time constraint.

**2. Tests vs. time**
I believe tests should be written alongside the code, not after. I actually started
writing unit and integration tests for the transcription service, but decided to
stop — this is a time-boxed assignment and a working demo takes priority. If this
were a production project, tests would not be optional.

**3. Async vs. sync OpenAI client**
Considered using `AsyncOpenAI` since FastAPI supports async. Decided against it
because each request makes a single Whisper call with no parallelism needed —
async would add complexity in mocking and error handling with no real benefit at
this scale.

**4. Claude returning inconsistent JSON**
Sometimes Claude added markdown fences or text before the JSON. Solved by stripping
` ```json ``` ` fences with regex and finding the first `{` in the response.

**5. Word RTL alignment**
`python-docx` doesn't handle RTL cleanly. Added manual XML manipulation using
`OxmlElement` to set `w:bidi` and `w:jc right`. Consulted ChatGPT and Gemini —
both confirmed this is a known library limitation with no clean solution.
Decided not to spend more time on it given the time constraint.

**6. Whisper speaker identification**
Investigated whether Whisper could identify participants via API instructions.
Concluded it's not possible — Whisper does not support speaker diarization.
Tools like pyannote.audio or AssemblyAI would be needed. Since the assignment
says "use Whisper or any other solution you choose", I made a conscious decision
to stay with Whisper and handle the participants field via Claude's text analysis
instead — extracting names mentioned in the transcript rather than audio-level
speaker detection.

**7. Prompt refinement**
Spent time debating whether to keep iterating on the system prompt even after
results looked good. The prompt went through several iterations — adding language
detection rules, explicit fallback values, JSON structure enforcement, and
edge case handling for short or unclear transcripts. I stopped when the output
was consistently correct and well-structured across different inputs.

**8. Scope decisions**
Deliberately chose not to add features beyond the requirements (caching, deployed
demo, speaker diarization) to stay focused on delivering a complete, clean solution
within the time limit.



## Time Spent

~6 hours total:
- Day 1: ~3 hours (backend + frontend base)
- Day 2: ~2.5 hours (UI improvements, RTL support, Word export, prompt refinement)
- Day 2: ~0.5 hours (backend tests — unit and integration)
# AI Meeting Summarizer

A full-stack application that transcribes meeting recordings and generates
structured summaries using AI.

Upload an audio file (mp3 or wav) and get back a full transcript, meeting
summary, participants, decisions, and action items — with an option to download
as a Word document.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React + Vite |
| Backend | Python + FastAPI |
| Transcription | OpenAI Whisper API |
| Summarization | Anthropic Claude API |
| Word Export | python-docx |

---

## Prerequisites

You will need two API keys:
- **OpenAI API key** — for Whisper transcription → https://platform.openai.com
- **Anthropic API key** — for Claude summarization → https://console.anthropic.com

---

## Installation & Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/lilachKup/ai-meeting-summarizer.git
cd ai-meeting-summarizer
```

### 2. Backend setup

```bash
cd backend
python -m venv venv

# Mac/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file in the `backend` folder:
```
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
```

Start the backend:

```bash
uvicorn main:app --reload
```

Backend runs on http://localhost:8000

### 3. Frontend setup

Open a new terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on http://localhost:5173

---

## Usage

1. Open http://localhost:5173 in your browser
2. Click **Choose File** and upload an mp3 or wav recording
3. Wait for transcription and analysis (~10-20 seconds depending on file length)
4. View the summary, participants, decisions, and action items
5. Click **Download as Word** to save the results

---

## Running on a Different Machine

If you need to change ports or run on a remote server, update the values in:

**`backend/config.py`**
```python
ALLOWED_ORIGINS = ["http://localhost:5173"]  # Frontend URL
CLAUDE_MODEL = "claude-sonnet-4-6"           # Claude model to use
```

**`frontend/src/config.js`**
```js
const config = {
  API_BASE_URL: "http://localhost:8000/api",  // Backend URL
};
```

Also update `backend/config.py` and `frontend/src/config.js` — these are the only 
environment-specific values hardcoded outside of `.env`.

---

## Project Structure

```
ai-meeting-summarizer/
├── backend/
│   ├── config.py               # Environment-specific configuration
│   ├── main.py                 # FastAPI app entry point
│   ├── routes/
│   │   ├── transcribe.py       # POST /api/transcribe
│   │   └── summarize.py        # POST /api/summarize, /api/download
│   ├── services/
│   │   ├── whisper.py          # Whisper API integration
│   │   └── claude.py           # Claude API + system prompt
│   ├── utils/
│   │   └── docx_export.py      # Word file generation
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── config.js           # Environment-specific configuration
│       ├── api/
│       │   └── client.js       # All API calls
│       └── components/
│           ├── UploadForm.jsx
│           ├── ResultsPanel.jsx
│           └── DownloadButton.jsx
├── PROCESS.md
├── PROMPT.md
└── README.md
```

---

## Known Limitations

- Speaker identification is not supported — Whisper does not provide speaker
  diarization. Participants are extracted by Claude from names mentioned in
  the transcript text only.
- RTL alignment in the Word export is partially supported due to limitations
  in the python-docx library.
- Processing time depends on audio file length (Whisper) and transcript
  length (Claude).
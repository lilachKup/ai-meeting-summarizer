from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import transcribe #, summarize

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transcribe.router, prefix="/api")
# app.include_router(summarize.router, prefix="/api")
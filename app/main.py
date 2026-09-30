from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.routes import router

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="FitBuddy – AI Fitness Plan Generator",
    description="AI-powered 7-day fitness plan generator using Google Gemini, FastAPI, Jinja2 and SQLite.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
app.include_router(router)


@app.get("/health", tags=["System"])
def health():
    return {"status": "ok", "service": "FitBuddy"}

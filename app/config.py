import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent

load_dotenv(PROJECT_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{PROJECT_DIR / 'fitbuddy.db'}")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()

# The project specification names these Gemini models. They are configurable
# because Google can change model availability over time.
GEMINI_PRO_MODEL = os.getenv("GEMINI_PRO_MODEL", "gemini-3.5-flash-lite")
GEMINI_FLASH_MODEL = os.getenv("GEMINI_FLASH_MODEL", "gemini-3.5-flash-lite")

# Set DEMO_MODE=true if you want to test the complete UI/database flow
# without making Gemini API calls.
DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() in {"1", "true", "yes", "on"}

APP_NAME = "FitBuddy"

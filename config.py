"""Central settings. Values come from .env (copy .env-> .env and fill in)."""
import os
from dotenv import load_dotenv

load_dotenv()

# ---------- Gemini ----------
# Option A: AI Studio key (prototype)   -> set GEMINI_API_KEY
# Option B: Vertex AI (company data)    -> set USE_VERTEX=true, GCP_PROJECT, GCP_LOCATION
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "<YOUR_GEMINI_API_KEY>")
USE_VERTEX = os.getenv("USE_VERTEX", "false").lower() == "true"
GCP_PROJECT = os.getenv("GCP_PROJECT", "<YOUR_GCP_PROJECT_ID>")
GCP_LOCATION = os.getenv("GCP_LOCATION", "us-central1")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

# ---------- Local documents ----------
DOCS_DIR = os.getenv("DOCS_DIR", "./docs")

# ---------- Retrieval limits ----------
TOP_K_FILES = int(os.getenv("TOP_K_FILES", "5"))
MAX_CHARS_PER_FILE = int(os.getenv("MAX_CHARS_PER_FILE", "400000"))   # ~100k tokens
MAX_TOTAL_CHARS = int(os.getenv("MAX_TOTAL_CHARS", "2000000"))        # ~500k tokens
HISTORY_TURNS = int(os.getenv("HISTORY_TURNS", "6"))

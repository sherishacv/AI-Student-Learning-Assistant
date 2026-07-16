"""Application configuration and environment settings."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
VECTOR_STORE_DIR = BASE_DIR / "vector_store"
LOGS_DIR = BASE_DIR / "logs"
REPORTS_DIR = BASE_DIR / "reports"
TESTS_DIR = BASE_DIR / "tests"

load_dotenv(BASE_DIR / ".env")

PROJECT_NAME = "AI Student Learning Assistant"
DEFAULT_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1200"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
TOP_K = int(os.getenv("TOP_K", "5"))
HYBRID_ALPHA = float(os.getenv("HYBRID_ALPHA", "0.75"))
EMBEDDING_DIMENSION = 384


def ensure_directories() -> None:
    """Create required directories."""
    for path in [DATA_DIR, UPLOAD_DIR, VECTOR_STORE_DIR, LOGS_DIR, REPORTS_DIR, TESTS_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def get_env(name: str, default: str | None = None) -> str | None:
    """Read a configuration value safely from the environment."""
    value = os.getenv(name, default)
    return value if value not in {None, ""} else None

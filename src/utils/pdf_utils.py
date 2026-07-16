"""PDF ingestion helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pypdf import PdfReader

from src.utils.logger import configure_logger

logger = configure_logger("pdf_utils")


def extract_pdf_text(file_path: str | Path) -> list[dict[str, Any]]:
    """Extract text and page metadata from a PDF file."""
    path = Path(file_path)
    reader = PdfReader(str(path))
    pages: list[dict[str, Any]] = []
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            pages.append({"page": page_number, "content": text.strip(), "source": str(path)})
    logger.info("Extracted %d pages from %s", len(pages), path.name)
    return pages

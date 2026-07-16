"""PDF loader for the RAG pipeline."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.utils.logger import configure_logger
from src.utils.pdf_utils import extract_pdf_text

logger = configure_logger("rag.loader")


class PDFLoader:
    """Load PDF content and metadata."""

    def load(self, file_path: str | Path) -> list[dict[str, Any]]:
        """Load text from a PDF document."""
        pages = extract_pdf_text(file_path)
        logger.info("Loaded %d pages from %s", len(pages), Path(file_path).name)
        return pages

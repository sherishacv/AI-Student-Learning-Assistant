"""Utilities for loading and parsing PDF documents."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pypdf import PdfReadError, PdfReader

from config import configure_logging
from .exceptions import RAGError

logger = configure_logging("rag.pdf_loader")


class PDFDocumentLoader:
    """Loads text and page metadata from PDF files."""

    def __init__(self) -> None:
        self.logger = logger

    def load_documents(self, file_path: str | Path) -> list[dict[str, Any]]:
        """Extract text from a PDF and return a list of page-level documents."""
        path = Path(file_path)
        if not path.exists():
            raise RAGError(f"File not found: {path}")

        try:
            reader = PdfReader(str(path))
        except PdfReadError as exc:
            raise RAGError(f"Unable to read PDF: {path}") from exc

        documents: list[dict[str, Any]] = []
        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            if text.strip():
                documents.append(
                    {
                        "text": text.strip(),
                        "source": str(path),
                        "page_number": page_number,
                    }
                )

        if not documents:
            raise RAGError(f"No readable text found in document: {path}")

        self.logger.info("Loaded %d pages from %s", len(documents), path.name)
        return documents

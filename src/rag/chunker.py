"""Text chunking utilities for the RAG pipeline."""

from __future__ import annotations

from typing import Any

from config import CHUNK_OVERLAP, CHUNK_SIZE, configure_logging
from .exceptions import RAGError
from .models import DocumentChunk

logger = configure_logging("rag.chunker")


class TextChunker:
    """Splits document text into smaller overlapping chunks."""

    def __init__(self, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP) -> None:
        if chunk_size <= 0:
            raise RAGError("Chunk size must be greater than zero")
        if chunk_overlap < 0:
            raise RAGError("Chunk overlap cannot be negative")
        if chunk_overlap >= chunk_size:
            raise RAGError("Chunk overlap must be smaller than chunk size")

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.logger = logger

    def chunk_documents(self, documents: list[dict[str, Any]]) -> list[DocumentChunk]:
        """Split each page-level document into overlapping chunks."""
        chunks: list[DocumentChunk] = []

        for document in documents:
            words = document["text"].split()
            if not words:
                continue

            start = 0
            while start < len(words):
                end = min(start + self.chunk_size, len(words))
                chunk_words = words[start:end]
                chunk_text = " ".join(chunk_words).strip()

                if chunk_text:
                    chunk_id = f"{document['source']}-{document['page_number']}-{len(chunks)}"
                    chunk = DocumentChunk(
                        chunk_id=chunk_id,
                        text=chunk_text,
                        source=document["source"],
                        page_numbers=[document["page_number"]],
                        metadata={
                            "source": document["source"],
                            "page_number": document["page_number"],
                        },
                    )
                    chunks.append(chunk)

                if end == len(words):
                    break
                start = max(0, end - self.chunk_overlap)

        self.logger.info("Created %d chunks", len(chunks))
        return chunks

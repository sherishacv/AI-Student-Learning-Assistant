"""Data models used by the RAG pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class DocumentChunk:
    """Represents a chunk of text extracted and indexed from a document."""

    chunk_id: str
    text: str
    source: str
    page_numbers: list[int] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert the chunk to a serializable dictionary."""
        return {
            "chunk_id": self.chunk_id,
            "text": self.text,
            "source": self.source,
            "page_numbers": self.page_numbers,
            "metadata": self.metadata,
        }

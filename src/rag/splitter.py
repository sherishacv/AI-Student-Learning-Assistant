"""Recursive text splitting utilities."""

from __future__ import annotations

from typing import Any

from config import CHUNK_OVERLAP, CHUNK_SIZE


class RecursiveTextSplitter:
    """Split text into overlapping chunks."""

    def __init__(self, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP) -> None:
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, pages: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Split loaded pages into overlapping chunks."""
        chunks: list[dict[str, Any]] = []
        for page in pages:
            text = page["content"]
            words = text.split()
            if not words:
                continue
            start = 0
            index = 0
            while start < len(words):
                end = min(start + self.chunk_size, len(words))
                part = words[start:end]
                chunk_text = " ".join(part)
                if chunk_text:
                    chunks.append(
                        {
                            "content": chunk_text,
                            "source": page["source"],
                            "page": page["page"],
                            "chunk_id": f"{page['source']}-{page['page']}-{index}",
                        }
                    )
                if end == len(words):
                    break
                start = max(0, end - self.chunk_overlap)
                index += 1
        return chunks

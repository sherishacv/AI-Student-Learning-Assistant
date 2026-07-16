"""FAISS-backed vector store."""

from __future__ import annotations

import pickle
from pathlib import Path
from typing import Any

import faiss
import numpy as np

from config import EMBEDDING_DIMENSION, VECTOR_STORE_DIR


class FAISSVectorStore:
    """Persist embeddings and metadata in a FAISS index."""

    def __init__(self, index_path: str | Path | None = None) -> None:
        self.index_path = Path(index_path or VECTOR_STORE_DIR / "faiss.index")
        self.metadata_path = Path(VECTOR_STORE_DIR / "metadata.pkl")
        self.dimension = EMBEDDING_DIMENSION
        self.index: faiss.Index | None = None
        self.metadata: list[dict[str, Any]] = []
        self._initialize()

    def _initialize(self) -> None:
        """Create a new index or load an existing one."""
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        if self.index_path.exists() and self.metadata_path.exists():
            self.index = faiss.read_index(str(self.index_path))
            with self.metadata_path.open("rb") as handle:
                self.metadata = pickle.load(handle)
        else:
            self.index = faiss.IndexFlatL2(self.dimension)

    def add(self, embeddings: np.ndarray, chunks: list[dict[str, Any]]) -> None:
        """Add embeddings and chunk metadata to the index."""
        if self.index is None:
            raise RuntimeError("FAISS index is not initialized")
        self.index.add(np.asarray(embeddings, dtype=np.float32))
        self.metadata.extend(chunks)

    def search(self, embedding: np.ndarray, top_k: int = 5) -> list[tuple[float, dict[str, Any]]]:
        """Search nearest chunks."""
        if self.index is None or self.index.ntotal == 0:
            return []
        query = np.asarray(embedding, dtype=np.float32).reshape(1, -1)
        distances, indices = self.index.search(query, min(top_k, self.index.ntotal))
        results: list[tuple[float, dict[str, Any]]] = []
        for distance, index in zip(distances[0], indices[0]):
            if index < 0:
                continue
            results.append((float(distance), self.metadata[int(index)]))
        return results

    def save(self) -> None:
        """Persist index and metadata."""
        if self.index is None:
            return
        faiss.write_index(self.index, str(self.index_path))
        with self.metadata_path.open("wb") as handle:
            pickle.dump(self.metadata, handle)
    def clear(self) -> None:
        """Clear the current vector database."""
        self.index = faiss.IndexFlatL2(self.dimension)
        self.metadata = []

        if self.index_path.exists():
            self.index_path.unlink()

        if self.metadata_path.exists():
            self.metadata_path.unlink()
        self.save()
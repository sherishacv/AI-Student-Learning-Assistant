"""Sentence Transformer embeddings."""

from __future__ import annotations

import numpy as np
from sentence_transformers import SentenceTransformer

from config import EMBEDDING_DIMENSION, EMBEDDING_MODEL


class EmbeddingGenerator:
    """Generate dense embeddings for chunks and queries."""

    def __init__(self, model_name: str = EMBEDDING_MODEL) -> None:
        self.model = SentenceTransformer(model_name)

    def embed_texts(self, texts: list[str]) -> np.ndarray:
        """Embed a batch of texts."""
        embeddings = self.model.encode(texts, normalize_embeddings=True, convert_to_numpy=True)
        return np.asarray(embeddings, dtype=np.float32)

    def embed_query(self, query: str) -> np.ndarray:
        """Embed a single query."""
        embedding = self.embed_texts([query])[0]
        return np.asarray(embedding, dtype=np.float32)

    def dimension(self) -> int:
        """Return the embedding dimension."""
        return EMBEDDING_DIMENSION

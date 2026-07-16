"""Hybrid retrieval combining semantic and lexical signals."""

from __future__ import annotations

import re
from collections import Counter
from typing import Any

from config import HYBRID_ALPHA, TOP_K, configure_logging
from .embeddings import EmbeddingGenerator
from .vector_store import FAISSVectorStore

logger = configure_logging("rag.retriever")


class HybridRetriever:
    """Retrieves relevant chunks using dense and keyword-based scoring."""

    def __init__(self, vector_store: FAISSVectorStore, embedder: EmbeddingGenerator, alpha: float = HYBRID_ALPHA) -> None:
        self.vector_store = vector_store
        self.embedder = embedder
        self.alpha = alpha
        self.logger = logger

    def retrieve(self, query: str, top_k: int = TOP_K) -> list[dict[str, Any]]:
        """Retrieve a ranked list of relevant chunks for the query."""
        if not self.vector_store.chunks:
            return []

        query_embedding = self.embedder.embed_query(query)
        dense_results = self.vector_store.search(query_embedding, top_k=max(top_k * 3, 6))

        lexical_scores = {
            chunk.chunk_id: self._lexical_score(query, chunk.text)
            for chunk in self.vector_store.chunks
        }

        combined: dict[str, dict[str, Any]] = {}
        for result in dense_results:
            chunk = result["chunk"]
            combined[chunk.chunk_id] = {
                "chunk": chunk,
                "score": self.alpha * result["score"] + (1 - self.alpha) * lexical_scores.get(chunk.chunk_id, 0.0),
            }

        for chunk in self.vector_store.chunks:
            if chunk.chunk_id in combined:
                continue
            combined[chunk.chunk_id] = {
                "chunk": chunk,
                "score": (1 - self.alpha) * lexical_scores.get(chunk.chunk_id, 0.0),
            }

        ranked_results = sorted(combined.values(), key=lambda item: item["score"], reverse=True)
        self.logger.info("Retrieved %d chunks for query", len(ranked_results))
        return ranked_results[:top_k]

    def _lexical_score(self, query: str, text: str) -> float:
        """Compute a lightweight lexical overlap score."""
        query_terms = {term.lower() for term in re.findall(r"\w+", query)}
        if not query_terms:
            return 0.0

        text_terms = Counter(term.lower() for term in re.findall(r"\w+", text))
        matches = sum(text_terms[term] for term in query_terms if term in text_terms)
        return matches / max(1, len(query_terms))

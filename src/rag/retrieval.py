"""Hybrid retrieval layer."""

from __future__ import annotations

import re
from collections import Counter
from typing import Any

from config import HYBRID_ALPHA, TOP_K
from src.rag.embeddings import EmbeddingGenerator
from src.rag.vectorstore import FAISSVectorStore
from src.utils.helpers import extract_section_name


class HybridRetriever:
    """Retrieve relevant chunks using dense and keyword overlap scores."""

    def __init__(self, vector_store: FAISSVectorStore, embedder: EmbeddingGenerator, alpha: float = HYBRID_ALPHA) -> None:
        self.vector_store = vector_store
        self.embedder = embedder
        self.alpha = alpha

    def retrieve(self, query: str, top_k: int = TOP_K, intent: str | None = None) -> list[dict[str, Any]]:
        """Retrieve top-k chunks for a query."""
        if not self.vector_store.metadata:
            return []

        dense_results = self.vector_store.search(self.embedder.embed_query(query), top_k=max(top_k * 3, 10))
        lexical_scores = {
            item["chunk_id"]: self._keyword_score(query, item["content"])
            for item in self.vector_store.metadata
        }

        candidates: list[dict[str, Any]] = []
        for distance, chunk in dense_results:
            dense_score = 1.0 / (1.0 + max(float(distance), 1e-9))
            lexical_score = lexical_scores.get(chunk["chunk_id"], 0.0)
            agreement_score = self._agreement_score(chunk, dense_results)
            score = self.alpha * dense_score + (1.0 - self.alpha) * lexical_score + 0.05 * agreement_score
            candidates.append(
                {
                    "chunk": chunk,
                    "score": score,
                    "dense_score": dense_score,
                    "lexical_score": lexical_score,
                    "chunk_agreement": agreement_score,
                }
            )

        for chunk in self.vector_store.metadata:
            if any(candidate["chunk"]["chunk_id"] == chunk["chunk_id"] for candidate in candidates):
                continue
            lexical_score = lexical_scores.get(chunk["chunk_id"], 0.0)
            candidates.append(
                {
                    "chunk": chunk,
                    "score": (1.0 - self.alpha) * lexical_score,
                    "dense_score": 0.0,
                    "lexical_score": lexical_score,
                    "chunk_agreement": 0.0,
                }
            )

        if candidates:
            reference_chunk = max(candidates, key=lambda item: item["score"])["chunk"]
            reference_source = reference_chunk.get("source", "")
            reference_page = int(reference_chunk.get("page", 1))
            for candidate in candidates:
                chunk = candidate["chunk"]
                source_bonus = 0.06 if chunk.get("source", "") == reference_source else 0.0
                page_gap = abs(int(chunk.get("page", 1)) - reference_page)
                page_bonus = 0.04 / (1.0 + page_gap)
                candidate["score"] += source_bonus + page_bonus

        ranked = sorted(candidates, key=lambda item: item["score"], reverse=True)
        if intent and "summary" in intent.lower():
            return self._rank_for_summary(ranked, top_k)
        return self._merge_context_blocks(ranked, top_k)

    def _rank_for_summary(self, ranked: list[dict[str, Any]], top_k: int) -> list[dict[str, Any]]:
        """Favor chunks from the same source and nearby pages for chapter-level summaries."""
        return self._merge_context_blocks(ranked, top_k)

    def _merge_context_blocks(self, ranked: list[dict[str, Any]], top_k: int) -> list[dict[str, Any]]:
        """Merge nearby chunks from the same source into one richer context block."""
        deduped = self._deduplicate(ranked)
        grouped: list[list[dict[str, Any]]] = []
        for item in sorted(deduped, key=lambda entry: (entry["chunk"].get("source", ""), int(entry["chunk"].get("page", 1)), -entry["score"])):
            if not grouped:
                grouped.append([item])
                continue
            previous = grouped[-1][-1]
            previous_chunk = previous["chunk"]
            current_chunk = item["chunk"]
            same_source = current_chunk.get("source", "") == previous_chunk.get("source", "")
            page_gap = abs(int(current_chunk.get("page", 1)) - int(previous_chunk.get("page", 1)))
            if same_source and page_gap <= 1:
                grouped[-1].append(item)
            else:
                grouped.append([item])

        results: list[dict[str, Any]] = []
        for block in grouped[: max(top_k * 2, 6)]:
            first_chunk = block[0]["chunk"]
            merged_content = "\n\n".join(entry["chunk"]["content"] for entry in block)
            merged_content = merged_content[:2500]
            results.append(
                {
                    "content": merged_content,
                    "source": first_chunk.get("source", "unknown"),
                    "page": first_chunk.get("page", 1),
                    "section": extract_section_name(merged_content),
                    "relevance_score": round(sum(entry["score"] for entry in block) / max(1, len(block)), 3),
                    "semantic_score": round(sum(entry["dense_score"] for entry in block) / max(1, len(block)), 3),
                    "keyword_score": round(sum(entry["lexical_score"] for entry in block) / max(1, len(block)), 3),
                    "chunk_agreement": round(sum(entry.get("chunk_agreement", 0.0) for entry in block) / max(1, len(block)), 3),
                }
            )

        results = sorted(results, key=lambda entry: entry["relevance_score"], reverse=True)
        return results[:top_k]

    def _agreement_score(self, chunk: dict[str, Any], dense_results: list[tuple[float, dict[str, Any]]]) -> float:
        """Reward chunks that are near other strong dense matches."""
        if not dense_results:
            return 0.0
        same_source = sum(1 for _, item in dense_results if item.get("source", "") == chunk.get("source", ""))
        same_page = sum(1 for _, item in dense_results if int(item.get("page", 1)) == int(chunk.get("page", 1)))
        return round(min(1.0, (same_source / len(dense_results)) * 0.6 + (same_page / len(dense_results)) * 0.4), 3)

    def _deduplicate(self, ranked: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Remove duplicate chunks while preserving the highest scored version."""
        deduped: list[dict[str, Any]] = []
        seen: set[str] = set()
        for item in ranked:
            chunk = item["chunk"]
            if chunk["chunk_id"] in seen:
                continue
            deduped.append(item)
            seen.add(chunk["chunk_id"])
        return deduped

    def _keyword_score(self, query: str, text: str) -> float:
        """Compute a lightweight keyword overlap score."""
        query_terms = {term.lower() for term in re.findall(r"\w+", query)}
        if not query_terms:
            return 0.0
        counts = Counter(term.lower() for term in re.findall(r"\w+", text))
        matches = sum(counts[term] for term in query_terms if term in counts)
        return matches / max(1, len(query_terms))

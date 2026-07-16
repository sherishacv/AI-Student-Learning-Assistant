"""End-to-end RAG pipeline."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from config import TOP_K
from src.rag.embeddings import EmbeddingGenerator
from src.rag.loader import PDFLoader
from src.rag.retrieval import HybridRetriever
from src.rag.splitter import RecursiveTextSplitter
from src.rag.vectorstore import FAISSVectorStore
from src.utils.logger import configure_logger

logger = configure_logger("rag.pipeline")


class RAGPipeline:
    """Coordinate document loading, chunking, embedding, and retrieval."""

    def __init__(self) -> None:
        self.loader = PDFLoader()
        self.splitter = RecursiveTextSplitter()
        self.embedder = EmbeddingGenerator()
        self.vector_store = FAISSVectorStore()
        self.retriever = HybridRetriever(self.vector_store, self.embedder)

    def index_pdf(self, file_path: str | Path) -> None:
        self.vector_store.clear()
        """Load, split, embed, and store a PDF."""
        pages = self.loader.load(file_path)
        chunks = self.splitter.split(pages)
        if not chunks:
            raise ValueError("No content extracted from the PDF")
        embeddings = self.embedder.embed_texts([chunk["content"] for chunk in chunks])
        self.vector_store.add(embeddings, chunks)
        self.vector_store.save()
        logger.info("Indexed %s with %d chunks", Path(file_path).name, len(chunks))

    def retrieve(self, query: str, top_k: int = TOP_K, intent: str | None = None) -> list[dict[str, Any]]:
        """Retrieve the most relevant chunks for a query."""
        return self.retriever.retrieve(query, top_k=top_k, intent=intent)

    def get_state(self) -> dict[str, int]:
        """Return simple statistics about the current knowledge base."""
        return {
            "document_count": len({chunk["source"] for chunk in self.vector_store.metadata}),
            "chunk_count": len(self.vector_store.metadata),
        }

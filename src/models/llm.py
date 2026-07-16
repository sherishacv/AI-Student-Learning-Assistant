"""Language model wrapper for Groq."""

from __future__ import annotations

from typing import Any

from config import DEFAULT_MODEL, get_env
from src.utils.logger import configure_logger

logger = configure_logger("llm")


class GroqChatModel:
    """Thin wrapper around a chat model backend."""

    def __init__(self, model_name: str | None = None) -> None:
        self.model_name = model_name or DEFAULT_MODEL
        self.api_key = get_env("GROQ_API_KEY")
        self._client: Any | None = None

    def _get_client(self) -> Any:
        if self._client is None:
            try:
                from langchain_groq import ChatGroq
            except Exception as exc:  # pragma: no cover - defensive logging
                logger.warning("langchain-groq is not available: %s", exc)
                return None
            if not self.api_key:
                return None
            self._client = ChatGroq(model_name=self.model_name, groq_api_key=self.api_key)
        return self._client

    def invoke(self, prompt: str) -> str:
        """Invoke the configured chat model."""
        client = self._get_client()
        if client is None:
            return (
                "Groq model is unavailable. Configure GROQ_API_KEY to enable live generation."
            )
        try:
            response = client.invoke(prompt)
            return getattr(response, "content", str(response))
        except Exception as exc:  # pragma: no cover - defensive logging
            logger.exception("LLM invocation failed")
            return f"LLM invocation failed: {exc}"

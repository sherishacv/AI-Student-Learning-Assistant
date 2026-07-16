"""Flashcard generation agent."""

from __future__ import annotations

from typing import Any

from src.models.llm import GroqChatModel
from src.prompts.flashcard_prompt import flashcard_prompt
from src.utils.helpers import compute_confidence, sanitize_response


def flashcard_agent(state: dict[str, Any]) -> dict[str, Any]:
    """Create flashcards from retrieved context."""
    documents = state.get("retrieved_documents", [])
    context = "\n\n".join(doc["content"] for doc in documents)
    model = GroqChatModel()
    if not context:
        response = "I couldn't find this information in the uploaded study material."
    else:
        response = sanitize_response(model.invoke(flashcard_prompt(state.get("user_question", ""), context)))
    state["response"] = response
    state["confidence_score"] = compute_confidence(documents)
    state["selected_agent"] = "flashcard_agent"
    return state

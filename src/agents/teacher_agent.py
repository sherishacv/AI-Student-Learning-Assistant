"""Teacher agent."""

from __future__ import annotations

from typing import Any

from src.models.llm import GroqChatModel
from src.prompts.teacher_prompt import teacher_prompt
from src.utils.helpers import compute_confidence, sanitize_response


def teacher_agent(state: dict[str, Any]) -> dict[str, Any]:
    """Explain a concept using retrieved context."""
    documents = state.get("retrieved_documents", [])
    context = "\n\n".join(doc["content"] for doc in documents)
    model = GroqChatModel()
    if not context:
        response = "I couldn't find this information in the uploaded study material."
    else:
        response = sanitize_response(model.invoke(teacher_prompt(state.get("user_question", ""), context)))
    state["response"] = response
    state["confidence_score"] = compute_confidence(documents)
    state["selected_agent"] = "teacher_agent"
    return state

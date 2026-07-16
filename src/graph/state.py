"""State definition for the LangGraph workflow."""

from __future__ import annotations

from typing import TypedDict, List, Optional


class AgentState(TypedDict, total=False):
    """Shared state for the workflow."""

    user_question: str
    retrieved_documents: list[dict[str, object]]
    intent: str
    selected_agent: str
    response: str
    sources: list[str]
    pages: list[int]
    chat_history: list[dict[str, str]]
    confidence_score: float
    routing_logic: str
    response_time: float
    retrieved_chunks: list[str]

"""Intent routing for the LangGraph workflow."""

from __future__ import annotations

from typing import Any


def route_query(state: dict[str, Any]) -> str:
    """Route a user query to the appropriate agent."""
    intent = (state.get("intent") or "explain_topic").lower()
    if "quiz" in intent:
        return "quiz_agent"
    if "flashcard" in intent:
        return "flashcard_agent"
    if "summary" in intent:
        return "summary_agent"
    if "planner" in intent:
        return "planner_agent"
    if "doubt" in intent or "why" in intent or "how" in intent:
        return "doubt_solver_agent"
    return "teacher_agent"

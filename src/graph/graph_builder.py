"""Construct the LangGraph workflow."""

from __future__ import annotations

from typing import Any

from langgraph.graph import END, StateGraph

from src.agents.doubt_solver_agent import doubt_solver_agent
from src.agents.flashcard_agent import flashcard_agent
from src.agents.planner_agent import planner_agent
from src.agents.quiz_agent import quiz_agent
from src.agents.summary_agent import summary_agent
from src.agents.teacher_agent import teacher_agent
from src.graph.router import route_query
from src.graph.state import AgentState


def build_graph() -> Any:
    """Create and compile the workflow graph."""
    workflow = StateGraph(AgentState)

    workflow.add_node("teacher_agent", teacher_agent)
    workflow.add_node("quiz_agent", quiz_agent)
    workflow.add_node("flashcard_agent", flashcard_agent)
    workflow.add_node("summary_agent", summary_agent)
    workflow.add_node("planner_agent", planner_agent)
    workflow.add_node("doubt_solver_agent", doubt_solver_agent)

    workflow.set_entry_point("router")

    def router_node(state: dict[str, Any]) -> dict[str, Any]:
        selected = route_query(state)

        return {
            **state,
            "selected_agent": selected,
            "routing_logic": "keyword_router",
        }

    def route_to_agent(state: dict[str, Any]) -> str:
        return state["selected_agent"]

    workflow.add_node("router", router_node)

    workflow.add_conditional_edges(
        "router",
        route_to_agent,
        {
            "quiz_agent": "quiz_agent",
            "flashcard_agent": "flashcard_agent",
            "summary_agent": "summary_agent",
            "planner_agent": "planner_agent",
            "doubt_solver_agent": "doubt_solver_agent",
            "teacher_agent": "teacher_agent",
        },
    )

    workflow.add_edge("quiz_agent", END)
    workflow.add_edge("flashcard_agent", END)
    workflow.add_edge("summary_agent", END)
    workflow.add_edge("planner_agent", END)
    workflow.add_edge("doubt_solver_agent", END)
    workflow.add_edge("teacher_agent", END)

    return workflow.compile()
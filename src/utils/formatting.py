"""Formatting helpers for UI displays."""

from __future__ import annotations

from typing import Any


def bullet_list(items: list[Any]) -> str:
    """Render a bullet list."""
    return "\n".join(f"- {item}" for item in items)

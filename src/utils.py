"""Small formatting and validation helpers shared by the CLI."""

from __future__ import annotations

from typing import Iterable

from .models import Task


def format_task_table(tasks: Iterable[Task]) -> str:
    """Render tasks as a simple aligned text table."""
    rows = list(tasks)
    if not rows:
        return "No tasks found."
    lines = [str(task) for task in rows]
    return "\n".join(lines)


def parse_task_id(raw: str) -> int:
    try:
        return int(raw)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"'{raw}' is not a valid task id") from exc

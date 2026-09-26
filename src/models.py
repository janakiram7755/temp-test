"""Data model for a single task."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict

VALID_PRIORITIES = ("low", "medium", "high")


@dataclass
class Task:
    id: int
    title: str
    priority: str = "medium"
    done: bool = False

    def __post_init__(self) -> None:
        if self.priority not in VALID_PRIORITIES:
            raise ValueError(
                f"Invalid priority '{self.priority}'. "
                f"Must be one of {VALID_PRIORITIES}."
            )
        if not self.title or not self.title.strip():
            raise ValueError("Task title must not be empty.")

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        return cls(
            id=data["id"],
            title=data["title"],
            priority=data.get("priority", "medium"),
            done=data.get("done", False),
        )

    def mark_done(self) -> None:
        self.done = True

    def __str__(self) -> str:  # pragma: no cover - simple formatting
        status = "x" if self.done else " "
        return f"[{status}] #{self.id} ({self.priority}) {self.title}"

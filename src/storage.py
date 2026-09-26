"""JSON-backed storage for tasks, with atomic writes."""

from __future__ import annotations

import json
import os
import tempfile
from typing import List

from .models import Task

DEFAULT_PATH = "tasks.json"


class TaskStore:
    """Loads and persists a list of Task objects to a JSON file."""

    def __init__(self, path: str = DEFAULT_PATH) -> None:
        self.path = path
        self._tasks: List[Task] = []
        self._load()

    def _load(self) -> None:
        if not os.path.exists(self.path):
            self._tasks = []
            return
        with open(self.path, "r", encoding="utf-8") as fh:
            raw = json.load(fh) if os.path.getsize(self.path) else []
        self._tasks = [Task.from_dict(item) for item in raw]

    def _save(self) -> None:
        directory = os.path.dirname(os.path.abspath(self.path)) or "."
        fd, tmp_path = tempfile.mkstemp(dir=directory, prefix=".tasks-", suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                json.dump([t.to_dict() for t in self._tasks], fh, indent=2)
            os.replace(tmp_path, self.path)
        except Exception:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            raise

    def _next_id(self) -> int:
        return max((t.id for t in self._tasks), default=0) + 1

    def add(self, title: str, priority: str = "medium") -> Task:
        task = Task(id=self._next_id(), title=title, priority=priority)
        self._tasks.append(task)
        self._save()
        return task

    def list(self, pending_only: bool = False) -> List[Task]:
        if pending_only:
            return [t for t in self._tasks if not t.done]
        return list(self._tasks)

    def get(self, task_id: int) -> Task:
        for task in self._tasks:
            if task.id == task_id:
                return task
        raise KeyError(f"No task with id {task_id}")

    def complete(self, task_id: int) -> Task:
        task = self.get(task_id)
        task.mark_done()
        self._save()
        return task

    def remove(self, task_id: int) -> None:
        task = self.get(task_id)
        self._tasks.remove(task)
        self._save()

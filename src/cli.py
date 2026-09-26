"""Command-line interface for TaskLite."""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from .storage import TaskStore
from .utils import format_task_table


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tasklite", description="A tiny task manager.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")
    add_parser.add_argument(
        "--priority",
        choices=("low", "medium", "high"),
        default="medium",
        help="Task priority (default: medium)",
    )

    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument(
        "--pending-only", action="store_true", help="Only show incomplete tasks"
    )

    complete_parser = subparsers.add_parser("complete", help="Mark a task as done")
    complete_parser.add_argument("task_id", type=int, help="Task id")

    remove_parser = subparsers.add_parser("remove", help="Delete a task")
    remove_parser.add_argument("task_id", type=int, help="Task id")

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    store = TaskStore()

    if args.command == "add":
        task = store.add(args.title, priority=args.priority)
        print(f"Added task #{task.id}: {task.title}")
    elif args.command == "list":
        tasks = store.list(pending_only=args.pending_only)
        print(format_task_table(tasks))
    elif args.command == "complete":
        task = store.complete(args.task_id)
        print(f"Completed task #{task.id}: {task.title}")
    elif args.command == "remove":
        store.remove(args.task_id)
        print(f"Removed task #{args.task_id}")
    else:  # pragma: no cover - argparse enforces valid subcommands
        parser.print_help()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

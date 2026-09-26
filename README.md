# TaskLite

A tiny, dependency-free task manager for the command line.

TaskLite lets you add, list, complete, and remove tasks stored in a local
JSON file. It's intentionally small — a good example project for CI,
packaging, and testing experiments.

## Features

- Add tasks with a title and optional priority
- List all tasks, or only pending ones
- Mark tasks as complete
- Remove tasks by id
- Zero third-party dependencies (standard library only)

## Quick start

```bash
pip install -r requirements.txt   # no-op today, kept for future deps
python -m src.cli add "Write the quarterly report" --priority high
python -m src.cli list
python -m src.cli complete 1
```

See [docs/USAGE.md](docs/USAGE.md) for the full command reference.

## Development

```bash
python -m pytest tests/
```

## License

MIT — see [LICENSE](LICENSE).

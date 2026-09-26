# Usage

TaskLite is invoked as a Python module: `python -m src.cli <command> [options]`.

## Commands

### `add`

Add a new task.

```bash
python -m src.cli add "Buy milk"
python -m src.cli add "Ship the release" --priority high
```

Options:
- `--priority {low,medium,high}` — defaults to `medium`.

### `list`

List tasks.

```bash
python -m src.cli list
python -m src.cli list --pending-only
```

Options:
- `--pending-only` — only show tasks that aren't complete.

### `complete`

Mark a task as done by id.

```bash
python -m src.cli complete 3
```

### `remove`

Delete a task by id.

```bash
python -m src.cli remove 3
```

## Storage

Tasks are stored in `tasks.json` in the current working directory. The file
is created automatically on first use and rewritten atomically on every
change to avoid corruption.

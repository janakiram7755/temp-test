import json

import pytest

from src.cli import main


@pytest.fixture(autouse=True)
def _run_in_tmp_cwd(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    yield


def test_add_command(capsys):
    exit_code = main(["add", "Buy milk", "--priority", "high"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "Added task #1" in captured.out

    with open("tasks.json", encoding="utf-8") as fh:
        data = json.load(fh)
    assert data[0]["title"] == "Buy milk"
    assert data[0]["priority"] == "high"


def test_list_command_empty(capsys):
    exit_code = main(["list"])
    assert exit_code == 0
    assert "No tasks found." in capsys.readouterr().out


def test_complete_and_remove_flow(capsys):
    main(["add", "Task one"])
    main(["complete", "1"])
    captured = capsys.readouterr()
    assert "Completed task #1" in captured.out

    main(["remove", "1"])
    captured = capsys.readouterr()
    assert "Removed task #1" in captured.out

    with open("tasks.json", encoding="utf-8") as fh:
        data = json.load(fh)
    assert data == []


def test_list_pending_only(capsys):
    main(["add", "Pending task"])
    main(["add", "Done task"])
    main(["complete", "2"])
    capsys.readouterr()

    main(["list", "--pending-only"])
    out = capsys.readouterr().out
    assert "Pending task" in out
    assert "Done task" not in out

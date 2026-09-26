import pytest

from src.models import Task


def test_task_defaults():
    task = Task(id=1, title="Write docs")
    assert task.priority == "medium"
    assert task.done is False


def test_task_rejects_invalid_priority():
    with pytest.raises(ValueError):
        Task(id=1, title="Bad priority", priority="urgent")


def test_task_rejects_empty_title():
    with pytest.raises(ValueError):
        Task(id=1, title="   ")


def test_task_round_trip_dict():
    task = Task(id=2, title="Round trip", priority="high", done=True)
    data = task.to_dict()
    restored = Task.from_dict(data)
    assert restored == task


def test_task_mark_done():
    task = Task(id=3, title="Finish me")
    assert task.done is False
    task.mark_done()
    assert task.done is True

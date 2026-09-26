import os

import pytest

from src.storage import TaskStore


@pytest.fixture
def store_path(tmp_path):
    return str(tmp_path / "tasks.json")


def test_add_and_list(store_path):
    store = TaskStore(store_path)
    store.add("First task")
    store.add("Second task", priority="high")

    tasks = store.list()
    assert len(tasks) == 2
    assert tasks[0].title == "First task"
    assert tasks[1].priority == "high"


def test_persists_across_instances(store_path):
    store = TaskStore(store_path)
    store.add("Persisted task")

    reloaded = TaskStore(store_path)
    assert len(reloaded.list()) == 1
    assert reloaded.list()[0].title == "Persisted task"


def test_complete_task(store_path):
    store = TaskStore(store_path)
    task = store.add("Complete me")
    store.complete(task.id)

    assert store.get(task.id).done is True


def test_remove_task(store_path):
    store = TaskStore(store_path)
    task = store.add("Remove me")
    store.remove(task.id)

    with pytest.raises(KeyError):
        store.get(task.id)


def test_pending_only_filter(store_path):
    store = TaskStore(store_path)
    t1 = store.add("Pending")
    t2 = store.add("Done")
    store.complete(t2.id)

    pending = store.list(pending_only=True)
    assert [t.id for t in pending] == [t1.id]


def test_file_created_on_first_write(store_path):
    assert not os.path.exists(store_path)
    store = TaskStore(store_path)
    store.add("Creates file")
    assert os.path.exists(store_path)

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

from app import app as flask_app  # noqa: E402


@pytest.fixture
def client():
    flask_app.config.update({"TESTING": True})
    with flask_app.test_client() as client:
        yield client


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_get_tasks(client):
    resp = client.get("/tasks")
    assert resp.status_code == 200
    assert isinstance(resp.get_json(), list)


def test_get_single_task(client):
    resp = client.get("/tasks/1")
    assert resp.status_code == 200
    assert resp.get_json()["id"] == 1


def test_get_task_not_found(client):
    resp = client.get("/tasks/999")
    assert resp.status_code == 404


def test_create_task(client):
    resp = client.post("/tasks", json={"title": "Write docs"})
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["title"] == "Write docs"
    assert body["done"] is False


def test_create_task_missing_title(client):
    resp = client.post("/tasks", json={})
    assert resp.status_code == 400


def test_delete_task(client):
    create_resp = client.post("/tasks", json={"title": "Temp task"})
    task_id = create_resp.get_json()["id"]
    delete_resp = client.delete(f"/tasks/{task_id}")
    assert delete_resp.status_code == 200

    get_resp = client.get(f"/tasks/{task_id}")
    assert get_resp.status_code == 404


def test_delete_task_not_found(client):
    resp = client.delete("/tasks/9999")
    assert resp.status_code == 404

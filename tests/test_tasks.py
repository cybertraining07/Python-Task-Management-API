
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.exc import SQLAlchemyError

from main import app
from database import Base, get_db

# Create a separate in-memory database for testing
TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# Give every test a clean database
@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    yield


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_task():
    response = client.post(
        "/tasks",
        json={
            "title": "Learn Pytest",
            "description": "Write automated tests",
            "completed": False
        }
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Learn Pytest"


def test_get_all_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_existing_task():
    created = client.post(
        "/tasks",
        json={
            "title": "Test GET",
            "description": "Testing retrieval",
            "completed": False
        }
    )
    task_id = created.json()["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id


def test_update_task():
    created = client.post(
        "/tasks",
        json={
            "title": "Original Title",
            "description": "Testing update",
            "completed": False
        }
    )
    task_id = created.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"completed": True}
    )
    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_delete_task():
    created = client.post(
        "/tasks",
        json={
            "title": "Task to Delete",
            "description": "Testing deletion",
            "completed": False
        }
    )
    task_id = created.json()["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted successfully"

    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


def test_task_not_found():
    response = client.get("/tasks/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

def test_create_task_with_empty_title():
    response = client.post(
        "/tasks",
        json={
            "title": "",
            "description": "Invalid task",
            "completed": False
        }
    )

    assert response.status_code == 422


def test_create_task_with_whitespace_title():
    response = client.post(
        "/tasks",
        json={
            "title": "   ",
            "description": "Invalid task",
            "completed": False
        }
    )

    assert response.status_code == 422


def test_create_task_with_long_description():
    response = client.post(
        "/tasks",
        json={
            "title": "Valid task",
            "description": "A" * 501,
            "completed": False
        }
    )

    assert response.status_code == 422

def test_update_nonexistent_task():
    response = client.patch(
        "/tasks/999999",
        json={"completed": True}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_delete_nonexistent_task():
    response = client.delete("/tasks/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_update_task_with_empty_body():
    create_response = client.post(
        "/tasks",
        json={
            "title": "Error Handling Test",
            "description": "Testing empty updates",
            "completed": False
        }
    )

    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "No update fields provided"

def test_update_task_with_empty_title():
    create_response = client.post(
        "/tasks",
        json={"title": "Original title"}
    )

    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"title": ""}
    )

    assert response.status_code == 422


def test_update_task_with_whitespace_title():
    create_response = client.post(
        "/tasks",
        json={"title": "Original title"}
    )

    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"title": "   "}
    )

    assert response.status_code == 422


def test_update_task_with_long_description():
    create_response = client.post(
        "/tasks",
        json={"title": "Original title"}
    )

    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"description": "A" * 501}
    )

    assert response.status_code == 422


def test_update_task_with_null_title():
    create_response = client.post(
        "/tasks",
        json={"title": "Original title"}
    )

    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"title": None}
    )

    assert response.status_code == 422
def test_health_check_database_unavailable(monkeypatch):

    class BrokenDatabase:
        def execute(self, statement):
            raise SQLAlchemyError("Simulated database failure")

        def rollback(self):
            pass

    def override_broken_db():
        yield BrokenDatabase()

    monkeypatch.setitem(
        app.dependency_overrides,
        get_db,
        override_broken_db
    )

    response = client.get("/health")

    assert response.status_code == 503
    assert response.json()["detail"] == "Database unavailable"

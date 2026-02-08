"""
Test suite to verify multi-user isolation in the Todo API.
This ensures that users can only access their own tasks.
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool
from main import app
from models.user_task_models import User, Task, UserRole
from utils.auth import create_access_token
from datetime import timedelta
from uuid import uuid4


# Create an in-memory SQLite database for testing
@pytest.fixture(name="engine")
def fixture_engine():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(name="session")
def fixture_session(engine):
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def fixture_client(session):
    with TestClient(app) as client:
        yield client


def create_test_user(session, email: str, role: UserRole = UserRole.USER):
    """Helper to create a test user"""
    from utils.auth import hash_password

    user = User(
        email=email,
        password_hash=hash_password("testpassword"),
        first_name="Test",
        last_name="User",
        role=role
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def create_test_task(session, title: str, user_id: int, description: str = ""):
    """Helper to create a test task"""
    task = Task(
        title=title,
        description=description,
        user_id=user_id
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def get_auth_token(user_id: int):
    """Generate a JWT token for the given user"""
    return create_access_token(
        data={"sub": str(user_id)},
        expires_delta=timedelta(minutes=30)
    )


def test_user_can_access_own_tasks(client, session):
    """Test that a user can access their own tasks"""
    # Create two users
    user1 = create_test_user(session, "user1@example.com")
    user2 = create_test_user(session, "user2@example.com")

    # Create tasks for user1
    task1_user1 = create_test_task(session, "User 1 Task 1", user1.id, "Description for user 1 task 1")
    task2_user1 = create_test_task(session, "User 1 Task 2", user1.id, "Description for user 1 task 2")

    # Create tasks for user2
    task1_user2 = create_test_task(session, "User 2 Task 1", user2.id, "Description for user 2 task 1")

    # Get auth tokens for both users
    token_user1 = get_auth_token(user1.id)
    token_user2 = get_auth_token(user2.id)

    # User 1 should be able to access their own tasks
    response = client.get(
        f"/api/v1/users/{user1.id}/tasks",
        headers={"Authorization": f"Bearer {token_user1}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2  # User 1 has 2 tasks

    # Verify that the returned tasks belong to user1
    for task in data:
        assert task["user_id"] == user1.id


def test_user_cannot_access_other_users_tasks(client, session):
    """Test that a user cannot access another user's tasks"""
    # Create two users
    user1 = create_test_user(session, "user1@example.com")
    user2 = create_test_user(session, "user2@example.com")

    # Create tasks for user1
    task1_user1 = create_test_task(session, "User 1 Task 1", user1.id, "Description for user 1 task 1")

    # Create tasks for user2
    task1_user2 = create_test_task(session, "User 2 Task 1", user2.id, "Description for user 2 task 1")

    # Get auth tokens for both users
    token_user1 = get_auth_token(user1.id)
    token_user2 = get_auth_token(user2.id)

    # User 1 should NOT be able to access user 2's tasks
    response = client.get(
        f"/api/v1/users/{user2.id}/tasks",
        headers={"Authorization": f"Bearer {token_user1}"}
    )
    assert response.status_code == 403  # Forbidden

    # User 2 should NOT be able to access user 1's tasks
    response = client.get(
        f"/api/v1/users/{user1.id}/tasks",
        headers={"Authorization": f"Bearer {token_user2}"}
    )
    assert response.status_code == 403  # Forbidden


def test_user_cannot_view_individual_task_of_another_user(client, session):
    """Test that a user cannot view an individual task belonging to another user"""
    # Create two users
    user1 = create_test_user(session, "user1@example.com")
    user2 = create_test_user(session, "user2@example.com")

    # Create tasks for user1
    task1_user1 = create_test_task(session, "User 1 Task 1", user1.id, "Description for user 1 task 1")

    # Create tasks for user2
    task1_user2 = create_test_task(session, "User 2 Task 1", user2.id, "Description for user 2 task 1")

    # Get auth tokens for both users
    token_user1 = get_auth_token(user1.id)
    token_user2 = get_auth_token(user2.id)

    # User 1 should NOT be able to access user 2's specific task
    response = client.get(
        f"/api/v1/users/{user2.id}/tasks/{task1_user2.id}",
        headers={"Authorization": f"Bearer {token_user1}"}
    )
    assert response.status_code == 403  # Forbidden

    # User 2 should NOT be able to access user 1's specific task
    response = client.get(
        f"/api/v1/users/{user1.id}/tasks/{task1_user1.id}",
        headers={"Authorization": f"Bearer {token_user2}"}
    )
    assert response.status_code == 403  # Forbidden

    # But each user should be able to access their own task
    response = client.get(
        f"/api/v1/users/{user1.id}/tasks/{task1_user1.id}",
        headers={"Authorization": f"Bearer {token_user1}"}
    )
    assert response.status_code == 200
    assert response.json()["id"] == task1_user1.id

    response = client.get(
        f"/api/v1/users/{user2.id}/tasks/{task1_user2.id}",
        headers={"Authorization": f"Bearer {token_user2}"}
    )
    assert response.status_code == 200
    assert response.json()["id"] == task1_user2.id


def test_user_cannot_update_task_of_another_user(client, session):
    """Test that a user cannot update a task belonging to another user"""
    # Create two users
    user1 = create_test_user(session, "user1@example.com")
    user2 = create_test_user(session, "user2@example.com")

    # Create tasks for user1
    task1_user1 = create_test_task(session, "User 1 Task 1", user1.id, "Original description for user 1 task 1")

    # Create tasks for user2
    task1_user2 = create_test_task(session, "User 2 Task 1", user2.id, "Original description for user 2 task 1")

    # Get auth tokens for both users
    token_user1 = get_auth_token(user1.id)
    token_user2 = get_auth_token(user2.id)

    # User 1 should NOT be able to update user 2's task
    response = client.put(
        f"/api/v1/users/{user2.id}/tasks/{task1_user2.id}",
        headers={"Authorization": f"Bearer {token_user1}"},
        params={
            "title": "Updated by User 1",
            "description": "User 1 tried to update User 2's task"
        }
    )
    assert response.status_code == 403  # Forbidden

    # User 2 should NOT be able to update user 1's task
    response = client.put(
        f"/api/v1/users/{user1.id}/tasks/{task1_user1.id}",
        headers={"Authorization": f"Bearer {token_user2}"},
        params={
            "title": "Updated by User 2",
            "description": "User 2 tried to update User 1's task"
        }
    )
    assert response.status_code == 403  # Forbidden

    # But each user should be able to update their own task
    response = client.put(
        f"/api/v1/users/{user1.id}/tasks/{task1_user1.id}",
        headers={"Authorization": f"Bearer {token_user1}"},
        params={
            "title": "Updated by Owner",
            "description": "Owner updated their own task"
        }
    )
    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["title"] == "Updated by Owner"
    assert updated_task["description"] == "Owner updated their own task"


def test_user_cannot_delete_task_of_another_user(client, session):
    """Test that a user cannot delete a task belonging to another user"""
    # Create two users
    user1 = create_test_user(session, "user1@example.com")
    user2 = create_test_user(session, "user2@example.com")

    # Create tasks for user1
    task1_user1 = create_test_task(session, "User 1 Task 1", user1.id, "Description for user 1 task 1")

    # Create tasks for user2
    task1_user2 = create_test_task(session, "User 2 Task 1", user2.id, "Description for user 2 task 1")

    # Get auth tokens for both users
    token_user1 = get_auth_token(user1.id)
    token_user2 = get_auth_token(user2.id)

    # User 1 should NOT be able to delete user 2's task
    response = client.delete(
        f"/api/v1/users/{user2.id}/tasks/{task1_user2.id}",
        headers={"Authorization": f"Bearer {token_user1}"}
    )
    assert response.status_code == 403  # Forbidden

    # User 2 should NOT be able to delete user 1's task
    response = client.delete(
        f"/api/v1/users/{user1.id}/tasks/{task1_user1.id}",
        headers={"Authorization": f"Bearer {token_user2}"}
    )
    assert response.status_code == 403  # Forbidden

    # But each user should be able to delete their own task
    # First, create a new task for user 1 to delete
    task_to_delete = create_test_task(session, "Task to Delete", user1.id, "This will be deleted")

    response = client.delete(
        f"/api/v1/users/{user1.id}/tasks/{task_to_delete.id}",
        headers={"Authorization": f"Bearer {token_user1}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted successfully"


def test_admin_can_access_any_user_tasks(client, session):
    """Test that an admin user can access any user's tasks (if admin functionality exists)"""
    # Create admin user and regular user
    admin_user = create_test_user(session, "admin@example.com", UserRole.ADMIN)
    regular_user = create_test_user(session, "regular@example.com", UserRole.USER)

    # Create a task for the regular user
    task = create_test_task(session, "Regular User Task", regular_user.id, "Description for regular user task")

    # Get auth tokens
    token_admin = get_auth_token(admin_user.id)
    token_regular = get_auth_token(regular_user.id)

    # Admin should be able to access regular user's tasks
    response = client.get(
        f"/api/v1/users/{regular_user.id}/tasks",
        headers={"Authorization": f"Bearer {token_admin}"}
    )
    assert response.status_code == 200

    # Regular user should still not be able to access admin's tasks (unless admin has tasks)
    # Let's create a task for admin first
    admin_task = create_test_task(session, "Admin Task", admin_user.id, "Description for admin task")

    response = client.get(
        f"/api/v1/users/{admin_user.id}/tasks",
        headers={"Authorization": f"Bearer {token_regular}"}
    )
    assert response.status_code == 403  # Regular user can't access admin's tasks
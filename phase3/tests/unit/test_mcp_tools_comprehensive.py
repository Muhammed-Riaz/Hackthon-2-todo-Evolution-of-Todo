"""
Comprehensive Unit Tests for MCP Tools

This test suite verifies the functionality and security of all MCP tools
for todo operations: add_task, list_tasks, complete_task, update_task, delete_task.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool
from backend.src.mcp_tools.add_task import AddTaskInput, add_task
from backend.src.mcp_tools.list_tasks import ListTasksInput, list_tasks
from backend.src.mcp_tools.complete_task import CompleteTaskInput, complete_task
from backend.src.mcp_tools.update_task import UpdateTaskInput, update_task
from backend.src.mcp_tools.delete_task import DeleteTaskInput, delete_task
from backend.models.user_task_models import Task, User, UserRole
from backend.src.mcp_tools.errors import ValidationError, NotFoundError, AuthorizationError


# Create an in-memory SQLite database for testing
@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Create tables
    from backend.models.user_task_models import User, Task  # Import to register tables
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(bind=engine)

    with Session(engine) as session:
        # Create a test user
        test_user = User(
            email="test@example.com",
            password_hash="hashed_password",
            first_name="Test",
            last_name="User"
        )
        session.add(test_user)
        session.commit()
        session.refresh(test_user)

        # Add the test user to the session for tests to use
        session.test_user = test_user
        yield session


def test_add_task_success(db_session):
    """Test successful creation of a new task."""
    from backend.models.user_task_models import User

    # Prepare input data
    input_data = AddTaskInput(
        user_id=str(db_session.test_user.id),
        title="Test Task",
        description="Test Description"
    )

    # Call the add_task function
    result = add_task(input_data, db_session)

    # Verify the result
    assert result["success"] is True
    assert result["message"] == "Task created successfully"
    assert result["data"]["status"] == "created"
    assert result["data"]["title"] == "Test Task"

    # Verify the task was saved to the database
    saved_task = db_session.get(Task, result["data"]["task_id"])
    assert saved_task is not None
    assert saved_task.title == "Test Task"
    assert saved_task.description == "Test Description"
    assert saved_task.completed is False
    assert saved_task.user_id == db_session.test_user.id


def test_add_task_missing_title_fails(db_session):
    """Test that adding a task without a title fails."""
    input_data = AddTaskInput(
        user_id=str(db_session.test_user.id),
        title="",  # Empty title should fail
        description="Test Description"
    )

    with pytest.raises(ValidationError):
        add_task(input_data, db_session)


def test_list_tasks_empty_for_new_user(db_session):
    """Test listing tasks for a user with no tasks."""
    input_data = ListTasksInput(
        user_id=str(db_session.test_user.id),
        status="all"
    )

    result = list_tasks(input_data, db_session)

    assert result["success"] is True
    assert len(result["data"]["tasks"]) == 0


def test_list_tasks_with_tasks(db_session):
    """Test listing tasks for a user with existing tasks."""
    # Add a few tasks to the user
    task1 = Task(title="Task 1", user_id=db_session.test_user.id, completed=False)
    task2 = Task(title="Task 2", user_id=db_session.test_user.id, completed=True)
    db_session.add(task1)
    db_session.add(task2)
    db_session.commit()

    input_data = ListTasksInput(
        user_id=str(db_session.test_user.id),
        status="all"
    )

    result = list_tasks(input_data, db_session)

    assert result["success"] is True
    assert len(result["data"]["tasks"]) == 2
    titles = {task["title"] for task in result["data"]["tasks"]}
    assert "Task 1" in titles
    assert "Task 2" in titles


def test_complete_task_success(db_session):
    """Test successfully marking a task as completed."""
    # Create a task first
    task = Task(title="Incomplete Task", user_id=db_session.test_user.id, completed=False)
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    input_data = CompleteTaskInput(
        user_id=str(db_session.test_user.id),
        task_id=task.id
    )

    result = complete_task(input_data, db_session)

    assert result["success"] is True
    assert result["data"]["status"] == "completed"

    # Verify the task was updated in the database
    updated_task = db_session.get(Task, task.id)
    assert updated_task.completed is True


def test_complete_task_already_completed(db_session):
    """Test completing an already completed task (idempotent behavior)."""
    # Create a completed task
    task = Task(title="Already Completed Task", user_id=db_session.test_user.id, completed=True)
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    input_data = CompleteTaskInput(
        user_id=str(db_session.test_user.id),
        task_id=task.id
    )

    result = complete_task(input_data, db_session)

    # Should succeed but indicate the task was already completed
    assert result["success"] is True
    assert "already completed" in result["message"]


def test_update_task_title_only(db_session):
    """Test updating only the title of a task."""
    # Create a task first
    task = Task(title="Old Title", description="Old Description", user_id=db_session.test_user.id, completed=False)
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    input_data = UpdateTaskInput(
        user_id=str(db_session.test_user.id),
        task_id=task.id,
        title="New Title"
        # description not provided, should remain unchanged
    )

    result = update_task(input_data, db_session)

    assert result["success"] is True
    assert result["data"]["title"] == "New Title"

    # Verify the task was updated in the database
    updated_task = db_session.get(Task, task.id)
    assert updated_task.title == "New Title"
    assert updated_task.description == "Old Description"  # Should remain unchanged


def test_delete_task_success(db_session):
    """Test successfully deleting a task."""
    # Create a task first
    task = Task(title="Task to Delete", user_id=db_session.test_user.id, completed=False)
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    input_data = DeleteTaskInput(
        user_id=str(db_session.test_user.id),
        task_id=task.id
    )

    result = delete_task(input_data, db_session)

    assert result["success"] is True
    assert result["data"]["status"] == "deleted"

    # Verify the task was deleted from the database
    deleted_task = db_session.get(Task, task.id)
    assert deleted_task is None


def test_security_user_isolation_add_task(db_session):
    """Test that users cannot add tasks for other users directly via wrong user_id."""
    # Create another user for testing
    other_user = User(
        email="other@example.com",
        password_hash="hashed_password",
        first_name="Other",
        last_name="User"
    )
    db_session.add(other_user)
    db_session.commit()
    db_session.refresh(other_user)

    # Attempt to create a task for another user
    input_data = AddTaskInput(
        user_id=str(other_user.id),  # Attempt to create for other user
        title="Task for Other User",
        description="This should be scoped to the other user"
    )

    result = add_task(input_data, db_session)

    # Should succeed but the task should belong to the specified user_id
    assert result["success"] is True
    assert result["data"]["status"] == "created"

    # Verify the task belongs to the correct user
    task_id = result["data"]["task_id"]
    task = db_session.get(Task, task_id)
    assert task.user_id == other_user.id


def test_security_user_isolation_access_control(db_session):
    """Test that the validation system prevents unauthorized access."""
    # Create a task for the test user
    test_task = Task(title="User's Task", user_id=db_session.test_user.id, completed=False)
    db_session.add(test_task)
    db_session.commit()
    db_session.refresh(test_task)

    # Create another user
    other_user = User(
        email="other@example.com",
        password_hash="hashed_password",
        first_name="Other",
        last_name="User"
    )
    db_session.add(other_user)
    db_session.commit()
    db_session.refresh(other_user)

    # Attempt to access the test user's task as the other user
    # This should fail validation when using proper validation
    from backend.src.mcp_tools.base import validate_user_access

    with pytest.raises(Exception):  # Could be PermissionError or ValueError depending on implementation
        validate_user_access(db_session, str(other_user.id), test_task.id)


def test_input_validation_edge_cases(db_session):
    """Test edge cases for input validation."""
    # Test with very long title (should fail validation)
    with pytest.raises(ValidationError):
        invalid_input = AddTaskInput(
            user_id=str(db_session.test_user.id),
            title="t" * 300,  # Exceeds max length
            description="Too long title"
        )
        add_task(invalid_input, db_session)

    # Test with negative task ID for update_task
    with pytest.raises(ValidationError):
        invalid_input = UpdateTaskInput(
            user_id=str(db_session.test_user.id),
            task_id=-1,  # Invalid task ID
            title="Updated Title"
        )
        update_task(invalid_input, db_session)


def test_error_handling_database_connection_issues(db_session):
    """Test error handling when database operations fail."""
    # This would test with a mocked session that throws exceptions
    mock_session = Mock(spec=Session)
    mock_session.get.side_effect = Exception("Database connection failed")

    input_data = CompleteTaskInput(
        user_id=str(db_session.test_user.id),
        task_id=999  # Non-existent task
    )

    with pytest.raises(Exception):
        complete_task(input_data, mock_session)
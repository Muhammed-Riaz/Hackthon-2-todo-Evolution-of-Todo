# Todo Manager Specification

## Overview
This specification defines a clean, reusable Task data model and an in-memory TodoManager class that handles all CRUD operations for tasks. The implementation will be used as part of a todo CLI application with future phases planned for web, database, and AI agent integration.

## Target Audience
- Claude Code (as implementation generator)
- Future hackathon phases (web, database, AI agents)

## Success Criteria

### Task Data Model
- A `Task` dataclass (or pydantic/SQLModel-compatible class) with fields:
  - `id` (int, auto-incremented)
  - `title` (str, required)
  - `description` (str, optional)
  - `completed` (bool, default False)

### TodoManager Class
A `TodoManager` class that maintains a private list of Task objects and provides methods:

1. `add_task(title: str, description: str = "") -> Task`
   - Creates a new task with an auto-incremented ID
   - Validates that title is not empty or whitespace-only

2. `get_all_tasks() -> list[Task]`
   - Returns all tasks in the manager

3. `get_task_by_id(task_id: int) -> Task | None`
   - Returns the task with the specified ID or None if not found

4. `update_task(task_id: int, title: str | None = None, description: str | None = None) -> Task | None`
   - Updates the specified task with new values
   - Only updates fields that are provided (not None)

5. `delete_task(task_id: int) -> bool`
   - Deletes the task with the specified ID
   - Returns True if deletion was successful, False otherwise

6. `toggle_complete(task_id: int) -> Task | None`
   - Toggles the completed status of the specified task
   - Returns the updated task or None if task not found

### Additional Requirements
- All methods include proper type hints and docstrings
- Methods raise meaningful exceptions (e.g., ValueError for invalid ID or empty title)
- ID generation is automatic, sequential, and starts from 1
- Code follows PEP 8 standards and uses meaningful names
- Code is fully testable in isolation

## Constraints

### Implementation Files
- Implementation file: `src/todo_manager.py` (export TodoManager and Task)
- Separate models file: `src/models.py` (define Task class/dataclass)

### Technical Constraints
- Use only Python standard library (no external dependencies like pydantic yet – keep it pure stdlib for Phase I)
- Task title must not be empty or whitespace-only (validation in add/update)
- All public methods must handle invalid inputs gracefully and return appropriate values
- Code must be 100% generated from this spec by Claude Code

## Not Building
- Any CLI or user interface code
- Persistence to file/database
- Priority, tags, due dates, or any intermediate/advanced features
- Sorting, filtering, or searching logic
- Any integration with external APIs or AI agents

## Acceptance Criteria

### Task Model
- [ ] Task class has id (int), title (str), description (str, optional), completed (bool) attributes
- [ ] id is auto-incremented when creating new tasks
- [ ] title is required and cannot be empty or whitespace-only
- [ ] completed defaults to False

### TodoManager
- [ ] add_task creates new tasks with auto-incremented IDs
- [ ] get_all_tasks returns all tasks
- [ ] get_task_by_id returns specific task or None if not found
- [ ] update_task updates specified fields without affecting others
- [ ] delete_task removes task and returns success status
- [ ] toggle_complete toggles completion status
- [ ] All methods have proper type hints and docstrings
- [ ] All methods handle invalid inputs gracefully
- [ ] All methods follow PEP 8 standards
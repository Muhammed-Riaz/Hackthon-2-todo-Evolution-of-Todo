# Todo Manager API Contract

## Overview
This document defines the contract for the TodoManager class API, specifying the interface and expected behavior for all methods.

## Methods

### add_task(title: str, description: str = "") -> Task
**Purpose**: Creates a new task with an auto-incremented ID
**Parameters**:
- title (str): Required title of the task (cannot be empty or whitespace-only)
- description (str, optional): Optional description of the task (default: "")

**Returns**: Task object with auto-incremented ID and completed status set to False

**Exceptions**:
- ValueError: If title is empty or contains only whitespace

**Post-condition**: New task is added to the internal task list with the next available ID

### get_all_tasks() -> list[Task]
**Purpose**: Returns all tasks in the manager
**Parameters**: None
**Returns**: List of all Task objects in the manager (may be empty)
**Exceptions**: None

### get_task_by_id(task_id: int) -> Task | None
**Purpose**: Returns the task with the specified ID or None if not found
**Parameters**:
- task_id (int): The ID of the task to retrieve

**Returns**: Task object if found, None otherwise
**Exceptions**: None

### update_task(task_id: int, title: str | None = None, description: str | None = None) -> Task | None
**Purpose**: Updates the specified task with new values
**Parameters**:
- task_id (int): The ID of the task to update
- title (str | None): New title (only updates if provided and not None)
- description (str | None): New description (only updates if provided and not None)

**Returns**: Updated Task object if successful, None if task not found
**Exceptions**:
- ValueError: If title is provided but is empty or contains only whitespace

**Post-condition**: Only provided fields are updated; other fields remain unchanged

### delete_task(task_id: int) -> bool
**Purpose**: Deletes the task with the specified ID
**Parameters**:
- task_id (int): The ID of the task to delete

**Returns**: True if deletion was successful, False if task not found
**Exceptions**: None

**Post-condition**: Task is removed from internal task list if it existed

### toggle_complete(task_id: int) -> Task | None
**Purpose**: Toggles the completed status of the specified task
**Parameters**:
- task_id (int): The ID of the task to toggle

**Returns**: Updated Task object if successful, None if task not found
**Exceptions**: None

**Post-condition**: Completed status is flipped from current value

## Task Data Model Contract

### Task Fields
- id (int): Auto-incremented unique identifier, positive integer
- title (str): Required title, non-empty and not whitespace-only
- description (str): Optional description, may be empty string
- completed (bool): Status flag, defaults to False

## Error Handling Contract
- All public methods handle invalid inputs gracefully
- Methods return appropriate values (None for not found, boolean for success/failure)
- Meaningful exceptions are raised for invalid operations (e.g., ValueError for empty titles)
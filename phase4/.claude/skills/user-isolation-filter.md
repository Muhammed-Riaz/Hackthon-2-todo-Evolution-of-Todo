# User Isolation Filter Skill

**Name:** `user-isolation-filter`
**Description:** Always enforce that users can only see/modify their own tasks
**Version:** `1.0-phase2`

## Instructions

Apply user isolation filtering to EVERY database operation in Phase 2 Todo app.

## Core Principle

**Never trust user_id from request body or query parameters.**

Always use the `current_user_id` extracted from JWT authentication.

## Database Operation Patterns

### 1. List Tasks (GET /tasks)
```python
from sqlmodel import select

@router.get("/tasks")
async def list_tasks(
    current_user_id: str = Depends(get_current_user)
):
    # Always filter by current_user_id
    tasks = session.exec(
        select(Task).where(Task.user_id == current_user_id)
    ).all()
    return tasks
```

### 2. Get Single Task (GET /tasks/{task_id})
```python
@router.get("/tasks/{task_id}")
async def get_task(
    task_id: int,
    current_user_id: str = Depends(get_current_user)
):
    # Check ownership before returning
    task = session.get(Task, task_id)
    if not task or task.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task
```

### 3. Create Task (POST /tasks)
```python
@router.post("/tasks")
async def create_task(
    task_data: TaskCreate,
    current_user_id: str = Depends(get_current_user)
):
    # Always set user_id from JWT, never from request
    task = Task(
        title=task_data.title,
        description=task_data.description,
        user_id=current_user_id  # From JWT, not request body
    )
    session.add(task)
    session.commit()
    return task
```

### 4. Update Task (PUT /tasks/{task_id})
```python
@router.put("/tasks/{task_id}")
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user_id: str = Depends(get_current_user)
):
    # Check ownership before updating
    task = session.get(Task, task_id)
    if not task or task.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    # Update only allowed fields
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description

    session.commit()
    return task
```

### 5. Delete Task (DELETE /tasks/{task_id})
```python
@router.delete("/tasks/{task_id}")
async def delete_task(
    task_id: int,
    current_user_id: str = Depends(get_current_user)
):
    # Check ownership before deleting
    task = session.get(Task, task_id)
    if not task or task.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task"
        )

    session.delete(task)
    session.commit()
    return {"success": True}
```

### 6. Complete Task (PATCH /tasks/{task_id}/complete)
```python
@router.patch("/tasks/{task_id}/complete")
async def complete_task(
    task_id: int,
    current_user_id: str = Depends(get_current_user)
):
    # Check ownership before completing
    task = session.get(Task, task_id)
    if not task or task.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to complete this task"
        )

    task.completed = True
    session.commit()
    return task
```

## Security Rules

1. **Never trust client-provided user_id** - Always use JWT-extracted user_id
2. **Always filter queries** - Add `.where(Task.user_id == current_user_id)` to all queries
3. **Check ownership** - Verify user_id matches before update/delete/complete operations
4. **Return 403 Forbidden** - When user tries to access another user's tasks
5. **Return 404 Not Found** - When task doesn't exist (don't leak existence)

## Integration with Other Skills

- **JWT Auth**: Use `current_user_id` from `get_current_user` dependency
- **Error Handling**: Return appropriate HTTP status codes (403, 404)
- **Input Validation**: Combine with Pydantic validation for complete security

## Benefits

- **Data isolation** - Users can only access their own data
- **Security** - Prevents unauthorized access
- **Consistency** - Same pattern applied everywhere
- **Auditability** - Clear ownership tracking
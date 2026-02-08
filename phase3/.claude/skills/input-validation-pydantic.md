# Input Validation Pydantic Skill

**Name:** `input-validation-pydantic`
**Description:** Strict, consistent input validation pattern using Pydantic for FastAPI in Phase 2
**Version:** `1.0-phase2`

## Instructions

For every request body / query param in FastAPI, follow these validation patterns:

## Validation Rules

1. **Create dedicated Pydantic models** - Always use `BaseModel` for validation
2. **Use Field constraints** - Apply `min_length`, `max_length`, `pattern`, etc.
3. **Add descriptions** - Include `description` for OpenAPI documentation
4. **Prefer strict types** - Use `str` instead of `Any`, `positive int`, etc.
5. **Use validators** - Apply `validator` / `field_validator` for complex rules
6. **Automatic 422 errors** - Let FastAPI return detailed field validation errors

## Common Patterns for Todo App

### TaskCreate Model
```python
from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: str | None = Field(None, max_length=2000, description="Task description")
```

### TaskUpdate Model
```python
from pydantic import BaseModel, Field
from typing import Optional

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=2000, description="Task description")
```

## Security Note

- **user_id** always comes from JWT token
- **NEVER** accept user_id from request body
- Use FastAPI dependency injection to extract user_id from JWT

## Example Implementation

```python
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

router = APIRouter()

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: str | None = Field(None, max_length=2000, description="Task description")

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=2000, description="Task description")

@router.post("/tasks")
async def create_task(
    task_data: TaskCreate,
    current_user_id: str = Depends(get_current_user)  # From JWT
):
    # user_id comes from JWT, not from request body
    task = await create_task_in_db(
        title=task_data.title,
        description=task_data.description,
        user_id=current_user_id
    )
    return task
```

## Benefits

- **Type safety** - Catches invalid data early
- **Automatic documentation** - OpenAPI docs generated from Field descriptions
- **Consistent validation** - Same rules applied everywhere
- **Security** - Prevents user_id injection attacks
- **Developer experience** - Clear error messages for API consumers
# Data Model: Todo In-Memory Python Console App

## Task Entity

### Fields
- **id** (int): Auto-incremented unique identifier for the task
- **title** (str): Required title of the task (cannot be empty or whitespace-only)
- **description** (str): Optional description of the task (default: empty string)
- **completed** (bool): Status of the task (default: False)

### Relationships
- No relationships with other entities (standalone entity)

### Validation Rules
- `id`: Must be a positive integer, auto-incremented from 1
- `title`: Cannot be empty or contain only whitespace characters
- `completed`: Boolean value, defaults to False

### State Transitions
- `incomplete` → `completed`: When toggle_complete is called on an incomplete task
- `completed` → `incomplete`: When toggle_complete is called on a completed task

## TodoManager Entity

### Fields
- **_tasks** (list[Task]): Private list storing all Task objects
- **_next_id** (int): Private counter for auto-incrementing task IDs, starts at 1

### Validation Rules
- All method parameters must be validated before processing
- Task IDs must exist before operations are performed on them
- Task titles must not be empty or whitespace-only when adding or updating

### State Transitions
- Task list grows when add_task is called
- Task list shrinks when delete_task is called
- Individual task states change when update_task or toggle_complete are called
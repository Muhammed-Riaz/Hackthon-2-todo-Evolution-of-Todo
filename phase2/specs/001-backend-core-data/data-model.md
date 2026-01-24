# Data Model: Backend Core & Data Layer

**Feature**: 001-backend-core-data

## Entities

### Task

**Description**: Represents a user's to-do item

**Fields**:
- `id`: Integer (Primary Key, Auto-increment)
- `title`: String (Required, Max length: 255)
- `description`: String (Optional, Max length: 1000)
- `completed`: Boolean (Default: False)
- `user_id`: String (Required, Foreign Key reference to User)
- `created_at`: DateTime (Auto-generated on creation)
- `updated_at`: DateTime (Auto-generated and updated on modification)

**Validation Rules**:
- `title` must not be empty
- `title` must be between 1 and 255 characters
- `description` can be empty or null
- `description` must not exceed 1000 characters
- `completed` must be boolean type
- `user_id` must not be empty
- `user_id` must be a valid identifier format

**Relationships**:
- Belongs to one User (via user_id foreign key)
- Each user can have multiple tasks

**State Transitions**:
- New task: `completed = False` by default
- Task completion: `completed` can be toggled to `True`
- Task reopening: `completed` can be toggled back to `False`

### User (Reference)

**Description**: Identified by user_id which serves as a foreign key to associate tasks with the correct user

**Fields** (Future implementation):
- `user_id`: String (Primary Key)
- Other user-related fields (to be defined in future spec)

## Database Schema

### Tasks Table
```
Table: tasks
- id (INTEGER, PRIMARY KEY, AUTO_INCREMENT)
- title (VARCHAR(255), NOT NULL)
- description (TEXT, NULL)
- completed (BOOLEAN, DEFAULT FALSE)
- user_id (VARCHAR(255), NOT NULL)
- created_at (TIMESTAMP, NOT NULL)
- updated_at (TIMESTAMP, NOT NULL)
```

### Indexes
- Primary key index on `id`
- Composite index on `user_id` and `id` for efficient user-specific queries
- Index on `completed` for filtering completed tasks

## Constraints
- All tasks must be associated with a valid user_id
- Title is required for all tasks
- User isolation: All queries must filter by user_id
- Created timestamp is set on insertion
- Updated timestamp is set on creation and every update
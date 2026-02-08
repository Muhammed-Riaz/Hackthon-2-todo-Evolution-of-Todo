# MCP Tools Documentation: Todo Operations

This document describes the MCP (Model Context Protocol) tools available for todo operations in the Todo CLI application.

## Overview

The MCP Task Server exposes todo operations as stateless tools that can be used by AI agents. Each tool follows a strict contract and maintains user isolation through user_id validation.

## Available Tools

### 1. add_task

**Description**: Creates a new todo item for a user.

**Parameters**:
- `user_id` (string, required): The ID of the user who owns the task
- `title` (string, required): The title of the task
- `description` (string, optional): A detailed description of the task

**Response**:
- `task_id` (int): The ID of the created task
- `status` (string): Status of the operation ('created')
- `title` (string): The title of the created task
- `user_id` (string): The user ID associated with the task

**Example**:
```json
{
  "user_id": "user-123",
  "title": "Buy groceries",
  "description": "Milk, bread, eggs"
}
```

### 2. list_tasks

**Description**: Retrieves a user's todo items with optional filtering.

**Parameters**:
- `user_id` (string, required): The ID of the user whose tasks to retrieve
- `status` (string, optional): Filter tasks by status ('all', 'pending', 'completed')

**Response**:
- Array of task objects containing `task_id`, `title`, `description`, `completed`, and `user_id`

**Example**:
```json
{
  "user_id": "user-123",
  "status": "pending"
}
```

### 3. complete_task

**Description**: Marks a task as completed.

**Parameters**:
- `user_id` (string, required): The ID of the user who owns the task
- `task_id` (int, required): The ID of the task to complete

**Response**:
- `task_id` (int): The ID of the completed task
- `status` (string): New status ('completed')
- `title` (string): Title of the completed task

**Example**:
```json
{
  "user_id": "user-123",
  "task_id": 42
}
```

### 4. update_task

**Description**: Updates the properties of a task.

**Parameters**:
- `user_id` (string, required): The ID of the user who owns the task
- `task_id` (int, required): The ID of the task to update
- `title` (string, optional): New title for the task
- `description` (string, optional): New description for the task

**Response**:
- `task_id` (int): The ID of the updated task
- `title` (string): Updated title
- `description` (string): Updated description
- `user_id` (string): User ID of the task owner

**Example**:
```json
{
  "user_id": "user-123",
  "task_id": 42,
  "title": "Updated task title"
}
```

### 5. delete_task

**Description**: Removes a task from the user's todo list.

**Parameters**:
- `user_id` (string, required): The ID of the user who owns the task
- `task_id` (int, required): The ID of the task to delete

**Response**:
- `success` (bool): Whether the deletion was successful

**Example**:
```json
{
  "user_id": "user-123",
  "task_id": 42
}
```

## Security and Validation

All MCP tools implement strict user validation:
- Each tool validates that the `user_id` matches the task's owner before performing operations
- Attempts to access or modify tasks belonging to other users will result in permission errors
- All parameters are validated for proper types and required fields

## Error Handling

All tools follow a consistent error handling approach:
- Invalid parameters return appropriate HTTP status codes (400 for bad request)
- Unauthorized access attempts return 403 Forbidden
- Database errors return 500 Internal Server Error with descriptive messages
- Missing resources return 404 Not Found

## Best Practices

1. Always include a `user_id` parameter when calling tools
2. Check the response status before assuming an operation succeeded
3. Handle error responses gracefully in your client code
4. Use appropriate status filters when retrieving tasks to optimize performance
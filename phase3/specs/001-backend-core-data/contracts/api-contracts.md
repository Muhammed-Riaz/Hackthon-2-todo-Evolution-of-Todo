# API Contracts: Task Management

**Feature**: 001-backend-core-data

## Overview

REST API for task management with user isolation. All endpoints require a user_id in the URL path to ensure proper data isolation between users.

## Endpoints

### 1. List User Tasks
- **Method**: GET
- **Path**: `/api/{user_id}/tasks`
- **Description**: Retrieve all tasks for a specific user
- **Parameters**:
  - `user_id` (path, required): User identifier
- **Response**: 200 OK
  - Body: Array of Task objects
- **Errors**:
  - 404: User not found
  - 500: Internal server error

### 2. Create Task
- **Method**: POST
- **Path**: `/api/{user_id}/tasks`
- **Description**: Create a new task for a user
- **Parameters**:
  - `user_id` (path, required): User identifier
- **Request Body**: TaskCreate object
  - `title` (string, required): Task title
  - `description` (string, optional): Task description
  - `completed` (boolean, optional): Completion status (defaults to false)
- **Response**: 201 Created
  - Body: Created Task object
- **Errors**:
  - 400: Invalid input data
  - 404: User not found
  - 500: Internal server error

### 3. Get Task
- **Method**: GET
- **Path**: `/api/{user_id}/tasks/{task_id}`
- **Description**: Retrieve details of a specific task
- **Parameters**:
  - `user_id` (path, required): User identifier
  - `task_id` (path, required): Task identifier
- **Response**: 200 OK
  - Body: Task object
- **Errors**:
  - 404: Task not found or doesn't belong to user
  - 500: Internal server error

### 4. Update Task
- **Method**: PUT
- **Path**: `/api/{user_id}/tasks/{task_id}`
- **Description**: Update details of a specific task
- **Parameters**:
  - `user_id` (path, required): User identifier
  - `task_id` (path, required): Task identifier
- **Request Body**: TaskUpdate object
  - `title` (string, optional): Task title
  - `description` (string, optional): Task description
  - `completed` (boolean, optional): Completion status
- **Response**: 200 OK
  - Body: Updated Task object
- **Errors**:
  - 400: Invalid input data
  - 404: Task not found or doesn't belong to user
  - 500: Internal server error

### 5. Delete Task
- **Method**: DELETE
- **Path**: `/api/{user_id}/tasks/{task_id}`
- **Description**: Delete a specific task
- **Parameters**:
  - `user_id` (path, required): User identifier
  - `task_id` (path, required): Task identifier
- **Response**: 200 OK
  - Body: Success confirmation object
- **Errors**:
  - 404: Task not found or doesn't belong to user
  - 500: Internal server error

### 6. Complete Task
- **Method**: PATCH
- **Path**: `/api/{user_id}/tasks/{task_id}/complete`
- **Description**: Toggle the completion status of a specific task
- **Parameters**:
  - `user_id` (path, required): User identifier
  - `task_id` (path, required): Task identifier
- **Response**: 200 OK
  - Body: Updated Task object
- **Errors**:
  - 404: Task not found or doesn't belong to user
  - 500: Internal server error

## Data Models

### Task Object
```
{
  "id": integer,
  "title": string,
  "description": string | null,
  "completed": boolean,
  "user_id": string,
  "created_at": string (ISO 8601 datetime),
  "updated_at": string (ISO 8601 datetime)
}
```

### TaskCreate Object
```
{
  "title": string,
  "description": string | null,
  "completed": boolean (optional, default: false)
}
```

### TaskUpdate Object
```
{
  "title": string (optional),
  "description": string | null (optional),
  "completed": boolean (optional)
}
```

### Success Response
```
{
  "success": boolean,
  "message": string (optional)
}
```

### Error Response
```
{
  "detail": string
}
```

## Authentication & Authorization

- For this spec: user_id is passed in the URL path and trusted as input
- All operations are scoped to the user_id in the URL
- Users can only access tasks that belong to their user_id
- Future specs will add JWT authentication to validate user identity
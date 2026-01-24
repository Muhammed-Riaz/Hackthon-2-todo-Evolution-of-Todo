# API Contracts: Authentication & API Security

**Feature**: 002-auth-security-jwt

## Overview

Enhanced API contracts with JWT-based authentication and authorization. All existing endpoints now require valid JWT tokens in the Authorization header. The system enforces that the user_id in the JWT token matches the user_id in the URL path.

## Authentication Endpoints

### 1. User Registration
- **Method**: POST
- **Path**: `/api/auth/register`
- **Description**: Register a new user via Better Auth
- **Headers**:
  - `Content-Type: application/json`
- **Request Body**:
  - `email` (string, required)
  - `password` (string, required)
  - `name` (string, optional)
- **Response**: 201 Created
  - Body: User object with JWT token
- **Errors**:
  - 400: Invalid input data
  - 409: Email already registered
  - 500: Internal server error

### 2. User Login
- **Method**: POST
- **Path**: `/api/auth/login`
- **Description**: Authenticate user and return JWT token
- **Headers**:
  - `Content-Type: application/json`
- **Request Body**:
  - `email` (string, required)
  - `password` (string, required)
- **Response**: 200 OK
  - Body: User object with JWT token
- **Errors**:
  - 400: Invalid credentials
  - 401: Unauthorized
  - 500: Internal server error

### 3. User Logout
- **Method**: POST
- **Path**: `/api/auth/logout`
- **Description**: Invalidate current session
- **Headers**:
  - `Authorization: Bearer {jwt_token}`
- **Response**: 200 OK
  - Body: Success confirmation
- **Errors**:
  - 401: Invalid or expired token
  - 500: Internal server error

## Protected Task Endpoints (Updated)

### 1. List User Tasks
- **Method**: GET
- **Path**: `/api/{user_id}/tasks`
- **Description**: Retrieve all tasks for a specific user
- **Headers**:
  - `Authorization: Bearer {jwt_token}`
- **Parameters**:
  - `user_id` (path, required): User identifier from JWT token
- **Response**: 200 OK
  - Body: Array of Task objects
- **Errors**:
  - 401: Invalid or expired token
  - 403: JWT user_id does not match URL user_id
  - 500: Internal server error

### 2. Create Task
- **Method**: POST
- **Path**: `/api/{user_id}/tasks`
- **Description**: Create a new task for a user
- **Headers**:
  - `Authorization: Bearer {jwt_token}`
  - `Content-Type: application/json`
- **Parameters**:
  - `user_id` (path, required): User identifier from JWT token
- **Request Body**: TaskCreate object
  - `title` (string, required)
  - `description` (string, optional)
  - `completed` (boolean, optional)
- **Response**: 201 Created
  - Body: Created Task object
- **Errors**:
  - 400: Invalid input data
  - 401: Invalid or expired token
  - 403: JWT user_id does not match URL user_id
  - 500: Internal server error

### 3. Get Task
- **Method**: GET
- **Path**: `/api/{user_id}/tasks/{task_id}`
- **Description**: Retrieve details of a specific task
- **Headers**:
  - `Authorization: Bearer {jwt_token}`
- **Parameters**:
  - `user_id` (path, required): User identifier from JWT token
  - `task_id` (path, required): Task identifier
- **Response**: 200 OK
  - Body: Task object
- **Errors**:
  - 401: Invalid or expired token
  - 403: JWT user_id does not match URL user_id or task doesn't belong to user
  - 404: Task not found
  - 500: Internal server error

### 4. Update Task
- **Method**: PUT
- **Path**: `/api/{user_id}/tasks/{task_id}`
- **Description**: Update details of a specific task
- **Headers**:
  - `Authorization: Bearer {jwt_token}`
  - `Content-Type: application/json`
- **Parameters**:
  - `user_id` (path, required): User identifier from JWT token
  - `task_id` (path, required): Task identifier
- **Request Body**: TaskUpdate object
  - `title` (string, optional)
  - `description` (string, optional)
  - `completed` (boolean, optional)
- **Response**: 200 OK
  - Body: Updated Task object
- **Errors**:
  - 400: Invalid input data
  - 401: Invalid or expired token
  - 403: JWT user_id does not match URL user_id or task doesn't belong to user
  - 404: Task not found
  - 500: Internal server error

### 5. Delete Task
- **Method**: DELETE
- **Path**: `/api/{user_id}/tasks/{task_id}`
- **Description**: Delete a specific task
- **Headers**:
  - `Authorization: Bearer {jwt_token}`
- **Parameters**:
  - `user_id` (path, required): User identifier from JWT token
  - `task_id` (path, required): Task identifier
- **Response**: 200 OK
  - Body: Success confirmation object
- **Errors**:
  - 401: Invalid or expired token
  - 403: JWT user_id does not match URL user_id or task doesn't belong to user
  - 404: Task not found
  - 500: Internal server error

### 6. Complete Task
- **Method**: PATCH
- **Path**: `/api/{user_id}/tasks/{task_id}/complete`
- **Description**: Toggle the completion status of a specific task
- **Headers**:
  - `Authorization: Bearer {jwt_token}`
- **Parameters**:
  - `user_id` (path, required): User identifier from JWT token
  - `task_id` (path, required): Task identifier
- **Response**: 200 OK
  - Body: Updated Task object
- **Errors**:
  - 401: Invalid or expired token
  - 403: JWT user_id does not match URL user_id or task doesn't belong to user
  - 404: Task not found
  - 500: Internal server error

## Data Models

### User Object
```
{
  "id": string,
  "email": string,
  "name": string | null,
  "created_at": string (ISO 8601 datetime),
  "updated_at": string (ISO 8601 datetime)
}
```

### JWT Token Response
```
{
  "user": User object,
  "token": string,
  "expires_at": string (ISO 8601 datetime)
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

## Authentication & Authorization Rules

- All protected endpoints require Authorization header with Bearer token
- JWT token must be properly signed with shared BETTER_AUTH_SECRET
- Token must not be expired
- User_id in JWT token must match user_id in URL path
- Users can only access their own data
- Invalid or missing tokens result in 401 Unauthorized
- Mismatched user_id results in 403 Forbidden
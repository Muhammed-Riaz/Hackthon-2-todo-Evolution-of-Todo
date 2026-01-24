# API Contracts: Frontend Application (Next.js + Better Auth)

## Authentication Endpoints

### POST /api/auth/signup
**Description**: Register a new user account

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "name": "John Doe"
}
```

**Response (Success)**:
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "user_abc123",
      "email": "user@example.com",
      "name": "John Doe"
    },
    "token": "jwt_token_here"
  }
}
```

**Response (Error)**:
```json
{
  "success": false,
  "error": "Email already exists"
}
```

### POST /api/auth/login
**Description**: Authenticate user and return session token

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (Success)**:
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "user_abc123",
      "email": "user@example.com",
      "name": "John Doe"
    },
    "token": "jwt_token_here"
  }
}
```

**Response (Error)**:
```json
{
  "success": false,
  "error": "Invalid credentials"
}
```

### POST /api/auth/logout
**Description**: End user session

**Headers**:
```
Authorization: Bearer {jwt_token}
```

**Response (Success)**:
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

## Task Management Endpoints

### GET /api/{user_id}/tasks
**Description**: Retrieve all tasks for the authenticated user

**Headers**:
```
Authorization: Bearer {jwt_token}
```

**Response (Success)**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "Complete project proposal",
      "description": "Finish the project proposal document",
      "completed": false,
      "userId": "user_abc123",
      "createdAt": "2023-10-15T10:30:00Z",
      "updatedAt": "2023-10-15T10:30:00Z"
    },
    {
      "id": 2,
      "title": "Schedule team meeting",
      "description": "Arrange meeting with team for project review",
      "completed": true,
      "userId": "user_abc123",
      "createdAt": "2023-10-14T09:15:00Z",
      "updatedAt": "2023-10-14T14:22:00Z"
    }
  ]
}
```

**Response (Error)**:
```json
{
  "success": false,
  "error": "Unauthorized access"
}
```

### POST /api/{user_id}/tasks
**Description**: Create a new task for the authenticated user

**Headers**:
```
Authorization: Bearer {jwt_token}
```

**Request**:
```json
{
  "title": "New task title",
  "description": "Detailed description of the task",
  "completed": false
}
```

**Response (Success)**:
```json
{
  "success": true,
  "data": {
    "id": 3,
    "title": "New task title",
    "description": "Detailed description of the task",
    "completed": false,
    "userId": "user_abc123",
    "createdAt": "2023-10-16T11:45:00Z",
    "updatedAt": "2023-10-16T11:45:00Z"
  }
}
```

**Response (Error)**:
```json
{
  "success": false,
  "error": "Invalid input data"
}
```

### GET /api/{user_id}/tasks/{id}
**Description**: Retrieve a specific task for the authenticated user

**Headers**:
```
Authorization: Bearer {jwt_token}
```

**Response (Success)**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Complete project proposal",
    "description": "Finish the project proposal document",
    "completed": false,
    "userId": "user_abc123",
    "createdAt": "2023-10-15T10:30:00Z",
    "updatedAt": "2023-10-15T10:30:00Z"
  }
}
```

**Response (Error)**:
```json
{
  "success": false,
  "error": "Task not found"
}
```

### PUT /api/{user_id}/tasks/{id}
**Description**: Update an existing task for the authenticated user

**Headers**:
```
Authorization: Bearer {jwt_token}
```

**Request**:
```json
{
  "title": "Updated task title",
  "description": "Updated description of the task",
  "completed": true
}
```

**Response (Success)**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Updated task title",
    "description": "Updated description of the task",
    "completed": true,
    "userId": "user_abc123",
    "createdAt": "2023-10-15T10:30:00Z",
    "updatedAt": "2023-10-16T12:00:00Z"
  }
}
```

**Response (Error)**:
```json
{
  "success": false,
  "error": "Task not found"
}
```

### DELETE /api/{user_id}/tasks/{id}
**Description**: Delete a specific task for the authenticated user

**Headers**:
```
Authorization: Bearer {jwt_token}
```

**Response (Success)**:
```json
{
  "success": true,
  "message": "Task deleted successfully"
}
```

**Response (Error)**:
```json
{
  "success": false,
  "error": "Task not found"
}
```

### PATCH /api/{user_id}/tasks/{id}/complete
**Description**: Toggle the completion status of a task for the authenticated user

**Headers**:
```
Authorization: Bearer {jwt_token}
```

**Response (Success)**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Complete project proposal",
    "description": "Finish the project proposal document",
    "completed": true,
    "userId": "user_abc123",
    "createdAt": "2023-10-15T10:30:00Z",
    "updatedAt": "2023-10-16T12:15:00Z"
  }
}
```

**Response (Error)**:
```json
{
  "success": false,
  "error": "Task not found"
}
```

## Error Response Format

All error responses follow this structure:

```json
{
  "success": false,
  "error": "Human-readable error message",
  "details": {
    // Optional field with additional error details
  }
}
```

## Authentication Requirements

- All task-related endpoints require a valid JWT token in the Authorization header
- The user_id in the URL must match the user_id in the JWT token
- Unauthorized requests return 401 status code
- Access to another user's tasks returns 403 status code
- Invalid tokens return 401 status code
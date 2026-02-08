# Data Model: Frontend Application (Next.js + Better Auth)

## Key Entities

### User
**Description**: Represents an authenticated user of the application with authentication credentials and session state

**Attributes**:
- id: Unique identifier for the user (string)
- email: Email address for login (string, required)
- name: User's display name (string, optional)
- createdAt: Timestamp when user account was created (ISO 8601 string)
- updatedAt: Timestamp when user account was last updated (ISO 8601 string)

**Validation Rules**:
- Email must be a valid email format
- Email must be unique across all users
- Name (if provided) must be between 1 and 100 characters

**State Transitions**:
- Unauthenticated → Authenticated (on successful login)
- Authenticated → Unauthenticated (on logout or token expiration)

### Task
**Description**: Represents a user's task item with properties like title, description, completion status, and association to a specific user

**Attributes**:
- id: Unique identifier for the task (integer)
- title: Brief title of the task (string, required)
- description: Detailed description of the task (string, optional)
- completed: Boolean indicating if task is completed (boolean, default: false)
- userId: Reference to the user who owns this task (string, required)
- createdAt: Timestamp when task was created (ISO 8601 string)
- updatedAt: Timestamp when task was last updated (ISO 8601 string)

**Validation Rules**:
- Title must be between 1 and 200 characters
- Description (if provided) must be between 1 and 1000 characters
- Completed must be a boolean value
- UserId must correspond to an authenticated user

**State Transitions**:
- Pending → Completed (when task is marked as done)
- Completed → Pending (when task is marked as undone)

## Relationships

### User → Task (One-to-Many)
- One user can own many tasks
- Tasks are always associated with a single user
- When user is deleted, all their tasks should also be deleted (cascade delete)

## Frontend State Models

### Session State
**Description**: Represents the current authentication state of the application

**Attributes**:
- isAuthenticated: Boolean indicating if user is currently authenticated (boolean)
- user: User object if authenticated, null otherwise (User object or null)
- isLoading: Boolean indicating if session is being checked (boolean)
- error: Error message if authentication failed (string or null)

### Task List State
**Description**: Represents the state of the task list view

**Attributes**:
- tasks: Array of task objects currently loaded (array of Task objects)
- isLoading: Boolean indicating if tasks are being loaded (boolean)
- error: Error message if task loading failed (string or null)
- filter: Current filter applied to task list (string: 'all', 'active', 'completed')

### API Response Format

#### Successful Response
```json
{
  "success": true,
  "data": { /* response data */ },
  "message": "Optional success message"
}
```

#### Error Response
```json
{
  "success": false,
  "error": "Error message",
  "details": { /* optional error details */ }
}
```

## Frontend Component Data Flow

### Authentication Components
- LoginForm: Receives email and password, returns user session
- SignupForm: Receives user details, creates new account and returns session
- AuthProvider: Manages global authentication state across the app

### Task Components
- TaskList: Receives array of tasks, emits events for task operations
- TaskItem: Receives individual task, emits events for task updates
- TaskForm: Handles task creation/editing, returns updated task data

## Validation Schema

### User Input Validation
- Email: Must match email regex pattern
- Password: Must be at least 8 characters with mixed case and numbers
- Task Title: Must be 1-200 characters, trimmed of whitespace
- Task Description: Must be 0-1000 characters

### Session Validation
- JWT token validity check
- Token expiration verification
- User ID consistency between token and API responses
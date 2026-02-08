# API Contracts: ChatKit Frontend

## Frontend → Backend Communication

### POST /api/{user_id}/chat
**Purpose**: Send user message to AI backend and receive response

**Request Headers**:
- Authorization: Bearer {jwt_token}
- Content-Type: application/json

**Path Parameters**:
- user_id (string): Authenticated user identifier from JWT

**Request Body**:
```json
{
  "conversation_id": 123,
  "message": "Add a task to buy groceries"
}
```

**Request Schema**:
```json
{
  "type": "object",
  "properties": {
    "conversation_id": {
      "type": "integer",
      "minimum": 1,
      "description": "Unique conversation identifier (omit for new conversation)"
    },
    "message": {
      "type": "string",
      "minLength": 1,
      "maxLength": 1000,
      "description": "User's message content"
    }
  },
  "required": ["message"],
  "additionalProperties": false
}
```

**Response Success (200)**:
```json
{
  "conversation_id": 123,
  "response": "I've added 'buy groceries' to your tasks.",
  "tool_calls": [
    {
      "name": "create_task",
      "arguments": {
        "title": "buy groceries",
        "user_id": "uuid-string"
      }
    }
  ]
}
```

**Response Schema**:
```json
{
  "type": "object",
  "properties": {
    "conversation_id": {
      "type": "integer",
      "minimum": 1,
      "description": "Conversation identifier (newly created if none was provided)"
    },
    "response": {
      "type": "string",
      "description": "AI's natural language response to the user"
    },
    "tool_calls": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string",
            "description": "Name of the MCP tool called"
          },
          "arguments": {
            "type": "object",
            "description": "Arguments passed to the MCP tool"
          }
        },
        "required": ["name", "arguments"]
      },
      "description": "Array of MCP tools called by the AI agent"
    }
  },
  "required": ["conversation_id", "response", "tool_calls"]
}
```

**Response Error (401)**:
```json
{
  "detail": "Unauthorized"
}
```

**Response Error (422)**:
```json
{
  "detail": "Validation Error"
}
```

**Response Error (500)**:
```json
{
  "detail": "Internal Server Error"
}
```

## Authentication Requirements

All requests to the chat endpoint must include:
- Valid JWT token in Authorization header
- user_id in path must match authenticated user
- Token must not be expired

## Expected Behavior

- If conversation_id is not provided, backend creates a new conversation
- Backend validates user_id matches authenticated user
- Response includes updated conversation_id for subsequent requests
- tool_calls array contains all MCP tools executed by the agent
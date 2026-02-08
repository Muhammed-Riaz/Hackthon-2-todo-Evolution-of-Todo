# Quickstart Guide: MCP Task Server

**Date**: 2026-02-03
**Feature**: MCP Task Server (Task Operations as Tools)

## Overview
This guide provides instructions for setting up and running the MCP Task Server that exposes task operations as tools for AI agents.

## Prerequisites
- Python 3.11+
- Poetry or pip for dependency management
- Access to Neon PostgreSQL database
- OpenAI API key (for agent integration)
- Official MCP SDK

## Environment Setup

### 1. Clone and Navigate to Project
```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Install Dependencies
```bash
# Using poetry
poetry install

# Or using pip
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file with the following variables:
```env
DATABASE_URL=postgresql://username:password@neon-host/db-name
OPENAI_API_KEY=your-openai-api-key
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=8000
```

## Running the MCP Task Server

### 1. Start the MCP Server
```bash
# If using a start script
python -m backend.src.mcp_server.server

# Or run directly
python backend/src/mcp_server/server.py
```

### 2. Verify MCP Tools are Available
Once running, the server will expose the following MCP tools:
- `add_task`: Create a new todo item
- `list_tasks`: Retrieve todos for a user
- `complete_task`: Mark a task as completed
- `update_task`: Update task title and/or description
- `delete_task`: Remove a task

## Using the MCP Tools

### Example Usage with OpenAI Agent
```python
from openai import OpenAI

client = OpenAI()

assistant = client.beta.assistants.create(
    model="gpt-4-turbo",
    tools=[
        {
            "type": "function",
            "function": {
                "name": "add_task",
                "description": "Create a new todo item",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string"},
                        "title": {"type": "string"},
                        "description": {"type": "string"}
                    },
                    "required": ["user_id", "title"]
                }
            }
        },
        # ... other tools
    ]
)
```

## Testing the Server

### Unit Tests
```bash
# Run all tests
pytest tests/

# Run specific MCP tools tests
pytest tests/mcp_tools/
```

### Integration Tests
```bash
# Run integration tests
pytest tests/integration/
```

## Troubleshooting

### Common Issues
1. **Database Connection Errors**: Verify DATABASE_URL is correctly set in environment
2. **MCP Tools Not Registering**: Check that all tools are properly decorated and registered with the MCP server
3. **User Validation Failures**: Ensure user_id format matches what's stored in the database

### Logging
The server logs all tool calls to help with debugging:
- Tool invocation metadata (tool name, user_id, timestamp)
- Request parameters
- Response payloads
- Error information (if applicable)

## Next Steps
- Integrate with the OpenAI Agent SDK
- Connect to the frontend chat interface
- Set up monitoring and alerting
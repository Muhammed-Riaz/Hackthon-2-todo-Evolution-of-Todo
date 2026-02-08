# Research: Agent & Chat Orchestration Implementation

**Date**: 2026-02-02
**Feature**: Agent & Chat Orchestration (AI Todo Chatbot)
**Researcher**: Claude

## Decision: Agent Configuration Strategy

**Decision**: Use OpenAI Assistants API with tool registration
**Rationale**: The OpenAI Assistants API provides a robust framework for defining system instructions, registering tools (MCP tools), and maintaining conversation context. This approach aligns with the architecture sketch that shows the agent runner with system context, conversation history, and MCP tool registry.
**Alternatives considered**:
- Custom agent implementation (too complex)
- LangChain agents (would require additional dependencies and learning curve)

## Decision: Conversation Data Persistence

**Decision**: Store conversation and message history in Neon PostgreSQL using SQLModel
**Rationale**: This follows the constitution's requirements for statelessness with database persistence. The system must reconstruct conversation state from database for each request, ensuring server restart safety.
**Alternatives considered**:
- In-memory storage (violates statelessness principle)
- Separate document store (adds complexity)

## Decision: Agent State Management

**Decision**: Stateless per-request execution with full conversation history reload
**Rationale**: Aligns with the constitution's "Statelessness First" principle and "Conversation Model" requirements. Each request is independently executable with conversation state reconstructed from database.
**Alternatives considered**:
- Session-based state (violates statelessness)
- Caching conversation context (could complicate restart safety)

## Decision: Error Handling Strategy

**Decision**: Agent-mediated friendly errors rather than exposing raw tool errors
**Rationale**: Provides better UX as specified in the input where option B (agent-mediated) was preferred over raw tool errors. The agent translates technical errors into user-friendly responses.
**Alternatives considered**:
- Raw tool error exposure (worse user experience)

## Decision: Multi-Tool Call Handling

**Decision**: Allow multiple tool calls per turn
**Rationale**: Supports natural language processing where a single user request might require multiple operations (e.g., "Add a task and show me all my tasks"). This enables better natural language support as mentioned in the input.
**Alternatives considered**:
- Single tool per request (limiting for natural language)

## OpenAI Agent Best Practices

**Research**: The OpenAI Assistants API is the recommended approach for building AI agents that need to call tools. It handles the complexity of determining which tools to call based on user input and manages the conversation flow.

**Best Practice**: Define clear system instructions that specify:
- The agent's role (todo assistant)
- How to use MCP tools for all task operations
- Response format expectations
- Error handling procedures

## MCP Tool Integration Patterns

**Research**: MCP tools must be registered with the OpenAI agent. The agent will decide when and how to call these tools based on user input. This fits the architecture where the agent runner has access to the MCP tool registry.

**Best Practice**: Ensure MCP tools return structured data that the agent can understand and incorporate into its natural language responses. The response aggregator should capture both the natural language response and tool call metadata.

## Database Schema Considerations

**Research**: Need to design conversation and message tables that support:
- User isolation via user_id
- Chronological ordering of messages
- Efficient retrieval of conversation history
- Support for optional conversation_id for thread management

**Best Practice**: Index appropriately for common query patterns (user_id, conversation_id, created_at). Ensure proper foreign key relationships between conversations and messages.

## Conversation Continuity Implementation

**Research**: For conversation continuity, the system needs to:
- Load full conversation history before agent execution
- Format history appropriately for the agent
- Append new messages after agent response
- Maintain context across multiple exchanges

**Best Practice**: Use a service layer that handles conversation loading/saving separately from the API endpoint logic. This ensures clean separation of concerns and testability.
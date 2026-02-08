# Research: MCP Task Server Implementation

**Date**: 2026-02-03
**Feature**: MCP Task Server (Task Operations as Tools)
**Researcher**: Claude

## Decision: Sync vs Async Tools

**Decision**: Sync SQLModel sessions
**Rationale**: Following the constitution's technical standards which specify that Phase II backend already uses sync SQLModel patterns. This maintains consistency with existing codebase and reduces complexity for the MCP tools. Since each tool call opens its own DB session anyway, the performance benefits of async are minimal for this use case.
**Alternatives considered**: Async sessions were considered for scalability but would introduce complexity that doesn't align with the stateless nature of MCP tools where each call is independent.

## Decision: Tool Return Payload Size

**Decision**: Minimal fields
**Rationale**: Following API best practices and the principle of returning only what's necessary. The specification already outlines what fields should be returned for each tool (task_id, status, title), which represents minimal information needed for agent operations. This reduces payload size and improves performance.
**Alternatives considered**: Full task objects would provide more information but violate the principle of minimal data transfer and could expose unnecessary information to the agent.

## Decision: Error Strategy

**Decision**: Return error objects inside normal responses
**Rationale**: MCP tools need to provide structured responses that AI agents can interpret reliably. Returning error information within the response structure allows the agent to handle errors programmatically without causing exceptions that might interrupt the conversation flow.
**Alternatives considered**: Raising MCP-native errors could interrupt the agent flow, while structured error responses within the normal payload allow for graceful error handling.

## Decision: Ownership Validation

**Decision**: Enforce ownership checks per task
**Rationale**: Security is paramount in the constitution's principles. Every operation must validate that the user_id in the request matches the task's owner in the database. This prevents cross-user data access which is a hard fail condition per the constitution.
**Alternatives considered**: Trusting user_id blindly would violate the security-aware AI design principle and could lead to data breaches.

## Decision: Pagination

**Decision**: No pagination (explicitly out of scope)
**Rationale**: The original specification and user stories don't indicate a need for pagination. The list_tasks operation returns all user tasks which should be manageable for typical todo list sizes. Adding pagination would increase complexity without clear benefit for the core use case.
**Alternatives considered**: Simple limit-based pagination was considered but rejected as scope creep for this initial implementation.

## MCP SDK Integration Patterns

**Research**: Official MCP SDK requires defining tools with specific input/output schemas. Each tool function will be decorated appropriately to register with the MCP server. The tools will be stateless functions that accept parameters and return structured data.

**Best Practice**: Each MCP tool should have clear input validation, perform its operation, and return a consistent response format. Error handling should be comprehensive but presented in a way that agents can understand and act upon.

## Database Session Management

**Research**: Each MCP tool call should open its own database session to maintain statelessness. The session should be properly closed after the operation completes. This aligns with the statelessness requirement in both the specification and constitution.

**Best Practice**: Use a session factory pattern that creates and tears down sessions per tool call. This ensures no state is maintained between calls while still providing proper transaction handling for each operation.

## OpenAI Agent Compatibility

**Research**: OpenAI Agents SDK expects tools to have well-defined schemas with clear input/output specifications. The MCP tools must be compatible with the agent's expectation of receiving structured responses that can be interpreted as part of the agent's reasoning process.

**Best Practice**: Each tool's input/output schema should be clearly defined using type hints and validation. Responses should include all necessary information for the agent to understand the outcome of the operation.
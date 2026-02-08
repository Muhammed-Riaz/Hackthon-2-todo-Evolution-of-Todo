<!-- SYNC IMPACT REPORT -->
<!-- Version change: 1.1.0 → 1.2.0 -->
<!-- Modified principles: Spec Supremacy, Agentic Purity, Traceable Development, Backend-First Reliability, Security-Aware Design, Deterministic Progression (adapted to AI context) -->
<!-- Added sections: AI-Native Architecture, MCP Integration, Statelessness, Agent Reasoning Isolation, Conversation Model, Data Integrity for AI -->
<!-- Removed sections: Authentication & Authorization Rules (replaced with AI-focused security) -->
<!-- Templates requiring updates: ✅ updated / ⚠ pending: .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md -->
<!-- Follow-up TODOs: None -->

# AI-Powered Todo Application with Conversational Interface Constitution (Phase III)

## Core Principles

### Spec Supremacy
The active spec is the single source of truth. No behavior, code, or configuration may exist without being explicitly specified. AI agent behaviors and MCP tool definitions must be documented in the spec.

### Agentic Purity
All implementation is produced by Claude Code. No manual code writing, editing, or hot-fixing is permitted outside the agent loop. All AI actions must occur through MCP tools with deterministic behavior.

### Traceable Development
Every artifact must trace to: Spec → Plan → Tasks → Implementation. Any output that cannot be traced is invalid. Agent reasoning must be auditable via tool_calls with full traceability.

### AI-Native Architecture
The system follows AI-native architecture using agents and tools, not hard-coded logic. MCP tools provide deterministic behavior while isolating probabilistic reasoning to the agent layer.

### Statelessness First
Servers must be stateless with state persisted only in the database. Conversation state must be reconstructed from database, and each request must be independently executable.

### Security-Aware AI Design
Security is built into the AI architecture from the start. Validate user_id on every operation, prevent cross-user data access, and ensure tool schemas are strictly enforced with no arbitrary code execution.

### Deterministic Progression
Each phase must be explicitly approved before advancing. No skipping, merging, or collapsing steps. AI agent implementations must be validated before frontend integration.

## Development Workflow Rules

The following loop is mandatory and immutable:

1. Spec Definition
2. Plan Generation
3. Task Decomposition
4. Implementation
5. Review → Next Spec

**🚫 Violations:**
- Planning without an approved spec
- Implementing without approved tasks
- Retroactively modifying specs to match code
- Bypassing MCP tools for database operations
- Hardcoding AI logic instead of using tools

## Technical Standards

### Frontend
- Framework: OpenAI ChatKit
- Authentication: Better Auth (JWT-ready)
- Token Handling: JWT via Authorization header
- AI Integration: MCP-compliant chat interface

### Backend
- Framework: Python FastAPI
- AI Framework: OpenAI Agents SDK
- MCP Server: Official MCP SDK
- ORM: SQLModel
- API Style: REST
- Async-first design where applicable
- Authentication: JWT verification only
- Authorization: JWT subject is authoritative

### Database
- Provider: Neon Serverless PostgreSQL
- Persistence: Required
- Data Ownership: User-scoped at query level
- Schema: Defined using SQLModel with explicit types
- Conversation State: Persisted in database with user_id scoping

### AI/MCP Layer
- All AI actions must occur through MCP tools
- MCP tools must be stateless and database-backed
- Agent reasoning must be auditable via tool_calls
- Tool schemas must be strictly enforced
- No execution of arbitrary code via agent

## AI Architecture Rules

### Agent Design Principles
- MCP tools must have deterministic behavior
- Probabilistic reasoning is isolated to agent layer only
- All tool calls must be logged for reproducibility and traceability
- Agent must not bypass MCP tools for data operations
- Backend must be restart-safe (no in-memory state)

### Conversation Model
- Server is stateless per request
- Conversation state reconstructed from database
- Each request is independently executable
- Multiple conversations per user supported
- Message history persisted in database

### Data Integrity for AI
- user_id must scope all data access
- Conversations and messages must be persisted
- Tasks must never be mutated outside MCP tools
- Agent must not bypass MCP tools
- All database operations must go through stateless MCP tools

## API Enforcement Rules

- All endpoints must strictly follow REST semantics
- Data models must be defined using SQLModel with explicit types
- All database queries must scope tasks by user_id
- API responses must use clear, consistent JSON schemas
- Errors must return correct HTTP status codes (400, 404, 500, etc.)
- MCP tools must validate user_id on every operation
- MCP tools must prevent cross-user data access

## Quality Gates (Hard Fail Conditions)

The project fails the spec if:
- Any MCP tool doesn't follow deterministic behavior
- Database queries don't properly scope tasks by user_id
- API responses don't use consistent JSON schemas
- Incorrect HTTP status codes are returned
- Manual code edits are detected
- Implementation deviates from approved plan or tasks
- Backend components are unstable or unreliable
- Agent bypasses MCP tools for data operations
- Conversation state is not properly persisted and reconstructed
- Tool schemas are not strictly enforced

## Success Criteria

- FastAPI server runs without errors
- MCP server runs without errors
- OpenAI Agent SDK integrates correctly
- All MCP tools function correctly against Neon PostgreSQL
- Conversations are correctly created, read, updated, and deleted
- Tasks are correctly managed through AI agent via MCP tools
- Tasks are always isolated by user_id
- APIs are testable via curl or Postman
- All 5 Basic Level features implemented as a web app with AI interface
- Complete spec → plan → task → implementation trail exists
- Project is reviewable, auditable, and reproducible
- Agent reasoning is traceable through tool_call logs

## Governance

This constitution supersedes all other practices. All development activities must verify compliance with these principles. Any deviation from these rules renders the implementation invalid. AI agent behaviors and MCP tool definitions must comply with the security and data integrity requirements outlined herein.

**Version**: 1.2.0 | **Ratified**: 2026-01-12 | **Last Amended**: 2026-02-03
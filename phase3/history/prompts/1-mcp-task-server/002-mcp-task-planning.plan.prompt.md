---
id: 002
title: MCP Task Planning
stage: plan
date: 2026-02-03
surface: agent
model: claude-sonnet-4-5-20250929
feature: 1-mcp-task-server
branch: 1-mcp-task-server
user: DELL
command: sp.plan
labels: [mcp, task-server, planning, architecture]
links:
  spec: specs/1-mcp-task-server/spec.md
  plan: specs/1-mcp-task-server/plan.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/1-mcp-task-server/plan.md
  - specs/1-mcp-task-server/research.md
  - specs/1-mcp-task-server/data-model.md
  - specs/1-mcp-task-server/contracts/mcp-tools-contracts.json
  - specs/1-mcp-task-server/quickstart.md
tests:
  - null
---

## Prompt

/sp.plan

Spec: Spec-4 — MCP Task Server (Task Operations as Tools)

Goal
Design and implement an MCP-compliant task server that exposes task CRUD
operations as stateless tools usable by OpenAI Agents, persisting all state
in Neon PostgreSQL via SQLModel.

────────────────────────────────
1. Architecture Sketch
────────────────────────────────

High-level flow:

AI Agent (OpenAI Agents SDK)
        │
        ▼
MCP Client (inside FastAPI backend)
        │
        ▼
MCP Server (Official MCP SDK)
        │
        ▼
Task Tools (add/list/update/complete/delete)
        │
        ▼
Database Layer (SQLModel + Neon PostgreSQL)

Key properties:
- MCP server is stateless (no in-memory task or conversation state)
- Each tool call opens its own DB session
- All validation and persistence happens per request
- Tools return structured JSON responses

────────────────────────────────
2. Section / Component Structure
────────────────────────────────

A. MCP Server Setup
- MCP server initialization
- Tool registration
- Tool schema definitions (input/output)

B. Database Integration
- SQLModel Task model reuse
- Session dependency factory (sync or async, consistent)
- Transaction handling per tool call

C. MCP Tools
- add_task
- list_tasks
- complete_task
- update_task
- delete_task

Each tool includes:
- Input validation
- Authorization check via user_id
- Database interaction
- Structured success/error response

D. Error Handling Layer
- Standard MCP error response format
- Domain errors (task not found, invalid input)
- Graceful failures for agent consumption

E. Observability
- Structured logging per tool call
- Tool invocation metadata (tool name, user_id, duration)

────────────────────────────────
3. Research-Concurrent Development Approach
────────────────────────────────

- Implement tools one-by-one while validating against MCP SDK docs
- Verify OpenAI Agents SDK compatibility during tool schema design
- Cross-check SQLModel patterns from Phase II backend
- Validate Neon Postgres constraints while implementing tools

No large upfront research phase — learning feeds directly into implementation.

────────────────────────────────
4. Key Design Decisions & Tradeoffs
────────────────────────────────

Decision: Sync vs Async Tools
- Option A: Sync SQLModel sessions (simpler, matches Phase II)
- Option B: Async sessions (more scalable, higher complexity)
→ Decision required before implementation

Decision: Tool Return Payload Size
- Minimal fields (id, title, status)
- Full task object
→ Tradeoff between agent clarity vs payload size

Decision: Error Strategy
- Raise MCP-native errors
- Return error objects inside normal responses
→ Impacts agent reasoning reliability

Decision: Ownership Validation
- Trust user_id blindly
- Enforce ownership checks per task
→ Security vs simplicity

Decision: Pagination
- No pagination (explicitly out of scope)
- Simple limit-based pagination
→ Must be locked to avoid scope creep

────────────────────────────────
5. Quality Validation (Acceptance Checks)
────────────────────────────────

Tool-Level Validation
- Each MCP tool callable independently
- All required parameters enforced
- Invalid inputs return structured errors

Behavior Validation
- add_task persists correctly
- list_tasks filters accurately
- update_task modifies only provided fields
- complete_task idempotent behavior defined
- delete_task permanently removes record

Stateles

## Response snapshot

Created a comprehensive implementation plan for the MCP Task Server. The plan includes:

- Technical Context with language, dependencies, and constraints
- Constitution Check verifying compliance with AI-native architecture and MCP integration requirements
- Project Structure outlining documentation and source code organization
- Research document resolving all key design decisions:
  - Sync SQLModel sessions chosen for consistency with existing codebase
  - Minimal return payloads to reduce data transfer
  - Error objects returned inside normal responses for agent compatibility
  - Ownership validation enforced per task for security
  - No pagination (explicitly out of scope)
- Data model defining Task, User, and MCP Tool entities with constraints
- API contracts with detailed schemas for all 5 MCP tools (add_task, list_tasks, complete_task, update_task, delete_task)
- Quickstart guide for setting up and running the MCP Task Server

The plan follows the layered architecture with MCP Server, Task Tools, and Database Layer, ensuring statelessness and proper user isolation as required by the constitution.

## Outcome

- ✅ Impact: Comprehensive MCP Task Server implementation plan created
- 🧪 Tests: null
- 📁 Files: plan.md, research.md, data-model.md, contracts/, quickstart.md created
- 🔁 Next prompts: Ready for task decomposition with /sp.tasks
- 🧠 Reflection: Plan addresses all key design decisions and aligns with constitution

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - Plan complete and compliant
- Prompt variant (if applicable): Standard planning workflow
- Next experiment (smallest change to try): Proceed to task decomposition
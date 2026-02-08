---
id: 001
title: AI Todo Constitution Update
stage: constitution
date: 2026-02-03
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: DELL
command: sp.constitution
labels: [constitution, ai, mcp, todo-app]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - .specify/templates/plan-template.md
  - .specify/templates/spec-template.md
  - .specify/templates/tasks-template.md
tests:
  - null
---

## Prompt

Project: AI-powered Todo Application with Conversational Interface (Phase III)

Purpose:
Extend the existing Todo backend and frontend with an AI-native,
stateless, natural-language chatbot using MCP (Model Context Protocol)
and OpenAI Agents SDK, following Agentic Dev Stack principles.

Core Principles:
- AI-native architecture (agents + tools, not hard-coded logic)
- Stateless servers, state persisted only in database
- Clear separation of concerns (API, Agent, MCP, DB)
- Deterministic tool behavior, probabilistic reasoning isolated to agent
- Reproducibility and traceability of agent actions (tool calls logged)
- No manual coding — all implementation via Claude Code

Key Standards:
- All AI actions must occur through MCP tools
- MCP tools must be stateless and database-backed
- Agent reasoning must be auditable via tool_calls
- Backend must be restart-safe (no in-memory state)
- APIs must be explicit, versionable, and testable

Architecture Constraints:
- Backend: FastAPI (Python)
- AI Framework: OpenAI Agents SDK
- MCP Server: Official MCP SDK
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Frontend: OpenAI ChatKit
- Auth: Better Auth (JWT-ready, even if partially implemented)

Data Integrity Rules:
- user_id must scope all data access
- Conversations and messages must be persisted
- Tasks must never be mutated outside MCP tools
- Agent must not bypass MCP tools

Conversation Model:
- Server is stateless per request
- Conversation state reconstructed from database
- Each request is independently executable
- Multiple conversations per user supported

Quality & Validation Standards:
- All specs must include:
  - Clear scope and non-scope
  - Acceptance criteria
  - Error handling expectations
- Each phase must be demoable independently
- Failures must be graceful and user-friendly

Security & Safety:
- Validate user_id on every operation
- Prevent cross-user data access
- No execution of arbitrary code via agent
- Tool schemas strictly enforced

Deliverable Standards:
- Clean repo structure:
  /fr

## Response snapshot

Updated the project constitution to reflect the AI-powered Todo Application with Conversational Interface (Phase III) requirements. The new constitution includes:

- Updated core principles to emphasize AI-native architecture, statelessness, and MCP integration
- Revised technical standards to include OpenAI Agents SDK, MCP Server, and ChatKit frontend
- Added AI-specific architecture rules for agent design, conversation model, and data integrity
- Updated quality gates to include MCP tool validation and conversation state requirements
- Modified success criteria to include MCP server functionality and agent reasoning traceability

Also updated dependent templates:
- plan-template.md: Added AI/MCP-specific constitution checks
- spec-template.md: Added AI/MCP-specific functional requirements
- tasks-template.md: Added foundational tasks for AI/MCP setup and implementation tasks for MCP tools

The constitution version was incremented from 1.1.0 to 1.2.0 to reflect the addition of new principles and material expansion of guidance.

## Outcome

- ✅ Impact: Updated constitution to support AI-powered Todo application with MCP integration
- 🧪 Tests: null
- 📁 Files: Updated constitution and 3 template files aligned with new principles
- 🔁 Next prompts: Continue with AI/MCP implementation following new constitution
- 🧠 Reflection: Constitution now properly supports AI-native architecture requirements

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - Constitution updated successfully
- Prompt variant (if applicable): Standard constitution update
- Next experiment (smallest change to try): Begin implementing AI/MCP features per new constitution
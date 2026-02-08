---
id: 1
title: update-project-constitution
stage: constitution
date: 2026-02-05
model: sonnet-4.5
surface: agent
feature: todo-ai-chatbot
branch: main
user: user
command: /sp.constitution
labels: ["constitution", "governance", "ai-agents", "mcp-tools"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests: []
---

# Update Project Constitution

## PROMPT_TEXT

```
Project: Phase III — Todo AI Chatbot (Agentic, MCP-based)

Mission:
Build a production-grade AI-powered Todo chatbot that enables users to manage tasks via natural language using OpenAI Agents, MCP tools, and a stateless FastAPI backend with persistent database-backed conversation history.

Core Principles:
- Agentic Dev Stack enforcement: specify → clarify → plan → task → implement
- No manual coding; all implementation via Claude Code
- Clear separation of concerns across frontend, backend, agent, MCP, and database
- Stateless servers; database is the only source of truth
- Tool-only authority: agents interact with tasks exclusively through MCP tools

Architecture Rules:
- Frontend (OpenAI ChatKit): UI-only, no business logic
- Chat API (/api/{user_id}/chat): orchestration only
- Agent (OpenAI Agents SDK): reasoning + MCP tool selection
- MCP Server (Official MCP SDK): task execution only
- Database (Neon PostgreSQL via SQLModel): persistence only

State Management:
- No in-memory or session state on server
- Conversation and message history persisted in database
- Server restarts must not affect conversations

MCP Constraints:
- All task CRUD operations exposed as MCP tools
- Tools are stateless, user-scoped, deterministic
- No REST or direct DB access by agents
- Each task mutation must correspond to an MCP tool call

Chat Orchestration:
- Single entry point: POST /api/{user_id}/chat
- Flow:
  1. Load conversation history
  2. Persist user message
  3. Run agent with MCP tools
  4. Persist assistant response
  5. Return response + tool calls
- No intent parsing in API layer

Frontend Rules:
- ChatKit sends messages and renders responses only
- No task logic, no tool interpretation, no state management

Authentication:
- user_id provided by upstream auth (Better Auth)
- MCP tools must re-verify user ownership
- Frontend must not fabricate user_id

Error Handling:
- Structured, explicit, user-safe errors
- Tool errors handled gracefully by agent
- No stack traces exposed to frontend

Scope:
In Scope
```

## RESPONSE_TEXT

Constitution file already exists with appropriate AI-powered Todo application principles. The constitution covers:
- AI-Native Architecture with MCP integration
- Statelessness First principles
- Security-Aware AI Design
- Agent Reasoning Isolation
- Conversation Model with proper state management
- Data Integrity for AI systems

The existing constitution addresses all the requirements from the user input including agentic development, MCP tools, stateless architecture, proper separation of concerns, and AI-specific security considerations.

## OUTCOME

Project constitution is properly configured for Phase III Todo AI Chatbot with MCP-based architecture. All principles aligned with AI agents, stateless design, and MCP tool constraints. No changes needed as the constitution already incorporates the required elements.
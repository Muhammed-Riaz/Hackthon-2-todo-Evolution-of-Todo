---
id: 1
title: Update Backend Constitution
stage: constitution
date: 2026-01-13
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 001-todo-web-app
user: claude
command: /sp.constituion Project: Full-Stack Multi-User Todo Web Application (Hackathon Project)
labels: [constitution, backend, data-layer, spec-1]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

```
/sp.constituion Project: Full-Stack Multi-User Todo Web Application (Hackathon Project)

Spec Focus: Spec 1 — Backend Core & Data Layer

Core principles:
- Correctness over speed (APIs must behave exactly as specified)
- Backend-first reliability (database + API stability is critical)
- Security-aware design (even before auth is added)
- Agentic development (spec → plan → tasks → implementation, no manual coding)

Key standards:
- All API endpoints must strictly follow REST semantics
- Data models must be defined using SQLModel with explicit types
- All database queries must scope tasks by user_id
- API responses must use clear, consistent JSON schemas
- Errors must return correct HTTP status codes (400, 404, 500, etc.)

Technology constraints:
- Backend framework: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Async-first design where applicable
- Environment variables for all secrets and database URLs

Functional requirements (Spec 1 scope only):
- Implement Task CRUD APIs:
  - GET    /api/{user_id}/tasks
  - POST   /api/{user_id}/tasks
  - GET    /api/{user_id}/tasks/{id}
  - PUT    /api/{user_id}/tasks/{id}
  - DELETE /api/{user_id}/tasks/{id}
  - PATCH  /api/{user_id}/tasks/{id}/complete
- Persist tasks in PostgreSQL
- Enforce task ownership using user_id at query level
- No authentication logic yet (user_id is trusted input for this spec)

Non-goals (explicitly out of scope):
- No frontend implementation
- No Better Auth or JWT verification
- No UI or session management
- No role-based access control

Quality constraints:
- Code must be production-ready, not demo-quality
- Database schema must support future auth integration
- Clear separation between models, routes, and services
- Minimal but sufficient logging

Success criteria:
- FastAPI server runs without errors
- All endpoints function correctly against Neon PostgreSQL
- Tasks are correctly created, read, updated, deleted, and toggled
- Tasks are always isolated by user_id
- APIs are testable via curl or Postman
```

## Response snapshot

Updated the project constitution to reflect the focus on backend core and data layer as specified in the requirements. The updated constitution emphasizes:

- Backend-first reliability as a core principle
- Strict adherence to REST semantics
- SQLModel with explicit types for data models
- User_id scoping for all database queries
- Consistent JSON schemas for API responses
- Correct HTTP status codes for errors
- Async-first design approach
- Production-ready code quality

The version has been incremented from 1.0.0 to 1.1.0 to reflect the addition of new principles and updates to existing ones to better align with the backend-focused requirements.

## Outcome

- ✅ Impact: Updated constitution to emphasize backend-first approach and data layer requirements
- 🧪 Tests: none
- 📁 Files: Modified .specify/memory/constitution.md
- 🔁 Next prompts: Ready to proceed with spec, plan, and task generation for backend implementation
- 🧠 Reflection: The constitution now properly reflects the backend and data layer focus for Spec 1

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): Begin spec generation for backend core implementation
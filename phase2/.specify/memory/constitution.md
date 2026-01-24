# Full-Stack Multi-User Todo Web Application Constitution

## Core Principles

### Spec Supremacy
The active spec is the single source of truth. No behavior, code, or configuration may exist without being explicitly specified.

### Agentic Purity
All implementation is produced by Claude Code. No manual code writing, editing, or hot-fixing is permitted outside the agent loop.

### Traceable Development
Every artifact must trace to: Spec → Plan → Tasks → Implementation. Any output that cannot be traced is invalid.

### Backend-First Reliability
Database and API stability is critical. All backend components must function correctly before frontend integration.

### Security-Aware Design
Security is built into the architecture from the start. Even before full authentication is added, security considerations guide design decisions.

### Deterministic Progression
Each phase must be explicitly approved before advancing. No skipping, merging, or collapsing steps.

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

## Technical Standards

### Frontend
- Framework: Next.js 16+
- Routing: App Router only
- Authentication: Better Auth
- Token Handling: JWT via Authorization header

### Backend
- Framework: Python FastAPI
- ORM: SQLModel
- API Style: REST
- Async-first design where applicable
- Authentication: JWT verification only (when implemented)
- Authorization: JWT subject is authoritative (when implemented)

### Database
- Provider: Neon Serverless PostgreSQL
- Persistence: Required
- Data Ownership: User-scoped at query level
- Schema: Defined using SQLModel with explicit types

## Authentication & Authorization Rules (Spec 1 - Future Implementation)

- Better Auth will issue JWT tokens
- JWT secret will be shared via: `BETTER_AUTH_SECRET`
- Backend must not:
  - Trust frontend user identity
  - Accept user IDs from request body
- Backend must:
  - Extract user identity from JWT
  - Enforce URL user_id === JWT subject
  - Reject unauthenticated requests with 401

## API Enforcement Rules (Spec 1 - Current Focus)

- All endpoints must strictly follow REST semantics
- Data models must be defined using SQLModel with explicit types
- All database queries must scope tasks by user_id
- API responses must use clear, consistent JSON schemas
- Errors must return correct HTTP status codes (400, 404, 500, etc.)
- For Spec 1 scope only: user_id is trusted input (authentication not yet implemented)

## Quality Gates (Hard Fail Conditions)

The project fails the spec if:
- Any endpoint doesn't follow REST semantics
- Database queries don't properly scope tasks by user_id
- API responses don't use consistent JSON schemas
- Incorrect HTTP status codes are returned
- Manual code edits are detected
- Implementation deviates from approved plan or tasks
- Backend components are unstable or unreliable

## Success Criteria

- FastAPI server runs without errors
- All endpoints function correctly against Neon PostgreSQL
- Tasks are correctly created, read, updated, deleted, and toggled
- Tasks are always isolated by user_id
- APIs are testable via curl or Postman
- All 5 Basic Level features implemented as a web app
- Complete spec → plan → task → implementation trail exists
- Project is reviewable, auditable, and reproducible

## Governance

This constitution supersedes all other practices. All development activities must verify compliance with these principles. Any deviation from these rules renders the implementation invalid.

**Version**: 1.1.0 | **Ratified**: 2026-01-12 | **Last Amended**: 2026-01-13

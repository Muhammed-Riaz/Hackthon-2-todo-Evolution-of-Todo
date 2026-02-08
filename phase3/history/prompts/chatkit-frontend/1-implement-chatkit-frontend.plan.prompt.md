---
id: 1
title: implement-chatkit-frontend
stage: plan
date: 2026-02-05
model: sonnet-4.5
feature: chatkit-frontend
branch: 006-chatkit-frontend
user: user
command: /sp.plan
labels: ["frontend", "chatkit", "ai-integration", "nextjs", "better-auth"]
links:
  spec: specs/006-chatkit-frontend/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/006-chatkit-frontend/plan.md
  - specs/006-chatkit-frontend/data-model.md
  - specs/006-chatkit-frontend/contracts/chat-api.md
  - specs/006-chatkit-frontend/quickstart.md
tests: []
---

# Implement ChatKit Frontend

## PROMPT_TEXT

```
Spec: Spec-6 — ChatKit Frontend (AI Chat UI Integration)

Goal:
Implement a ChatKit-based frontend that connects authenticated users
to the backend AI chat endpoint, enabling visible, persistent,
natural-language Todo interactions.

────────────────────────
Architecture Sketch
────────────────────────

Browser
  └── Next.js App Router
        └── /chat (page)
              ├── ChatKit UI
              ├── Auth session (Better Auth)
              ├── Chat API client
              └── UI-only state (messages, loading)

Chat Flow:
1. User opens /chat
2. Auth session resolves → user_id
3. ChatKit renders empty or existing conversation
4. User sends message
5. Frontend POSTs → /api/{user_id}/chat
6. Backend returns response + conversation_id
7. UI appends messages
8. conversation_id reused for next message

────────────────────────
Section / Component Structure
────────────────────────

Frontend Files:
- /app/chat/page.tsx
- /components/chat/ChatProvider.tsx
- /components/chat/ChatView.tsx
- /lib/chat/api.ts

Responsibilities:
- page.tsx → route + auth guard
- ChatProvider → conversation_id state
- ChatView → ChatKit UI rendering
- api.ts → POST /api/{user_id}/chat

────────────────────────
Implementation Phases
────────────────────────

Phase 1 — ChatKit Setup
- Install and configure OpenAI ChatKit
- Create base chat UI component
- Verify message input and render loop

Phase 2 — Auth Integration
- Resolve authenticated user_id via Better Auth
- Block unauthenticated access
- Inject user_id into API client

Phase 3 — Backend Binding
- Implement POST request to chat endpoint
- Handle conversation_id lifecycle
- Parse response and append messages

Phase 4 — UI State Handling
- Loading indicator while waiting for response
- Error bubble for failed requests
- Disable input during in-flight requests

Phase 5 — Persistence Validation
- Reload page → conversation continues
- New chat → conversation_id cleared
- Multiple messages render correctly

────────────────────────
Decisions Needing Documentation
────────────────────────

1. Conversation Storage
   - Option A: Local component state only
   - Option B: URL param (?conversation_id=)
   → Chosen: Component state (simpler, UI-only)

2. Message Rendering
   - Option A: Raw text only
   - Option B: Rich formatting
   → Chosen: Raw text (out of scope for Phase III)

3. Error Visibility
   - Option A: Silent retry
   - Option B: Explicit user message
   → Chosen: Explicit error message

────────────────────────
Quality Validation / Testing Strategy
────────────
```

## RESPONSE_TEXT

Created complete implementation plan for the ChatKit frontend including:
- Technical context with frontend/backend stack details
- Constitution check alignment
- Research findings with decision rationales
- Data model for conversation and message entities
- API contracts for the chat endpoint
- Quickstart guide for development setup
- Component architecture and responsibilities

## OUTCOME

Implementation plan is complete and ready for task breakdown and execution. The frontend is designed to integrate ChatKit with the AI backend while maintaining proper authentication and state management.
# Implementation Plan: ChatKit Frontend for AI Todo Chatbot

## Technical Context

**Feature**: ChatKit Frontend (AI Chat UI Integration)
**Branch**: 006-chatkit-frontend
**Spec**: specs/006-chatkit-frontend/spec.md
**Target Architecture**: Next.js 14+ with App Router, OpenAI ChatKit, Better Auth integration

**Frontend Stack**:
- Framework: Next.js 14+ with App Router
- UI Library: OpenAI ChatKit
- Auth: Better Auth (integrated with JWT)
- State Management: React hooks for UI-only state
- API Client: Built-in fetch for backend communication

**Backend Dependencies**:
- POST /api/{user_id}/chat endpoint
- Authentication via JWT tokens
- MCP tools for task operations
- Neon PostgreSQL database

**Integration Points**:
- Frontend authentication with Better Auth
- Backend API communication at /api/{user_id}/chat
- Conversation ID management between frontend and backend

## Constitution Check

This plan aligns with the project constitution by:
- Following the AI-Native Architecture principle by keeping agent logic isolated from the frontend
- Ensuring statelessness at the server level while maintaining UI state only on the client
- Using deterministic MCP tools for backend operations while isolating probabilistic reasoning to the agent layer
- Preserving user_id scoping for data access
- Following the Agentic Purity principle by implementing through Claude Code without manual intervention

## Development Gates

✅ **Prerequisites Satisfied**:
- Backend chat API endpoint exists at /api/{user_id}/chat
- Better Auth is configured for JWT authentication
- MCP tools are available for backend operations
- Neon PostgreSQL database is accessible

⚠️ **Risk Assessment**:
- Medium risk: ChatKit integration may have compatibility issues with current Next.js version
- Low risk: Auth integration should be straightforward given existing Better Auth setup

❌ **Blocking Issues**: None identified

## Phase 0: Research & Resolution

### research.md

#### Decision: ChatKit Package Selection
**Rationale**: Using OpenAI's official ChatKit library for the React-based chat interface
**Alternatives considered**: Custom-built chat UI, other third-party chat libraries
**Choice justified**: Official OpenAI solution with proper integration patterns

#### Decision: Authentication Flow Integration
**Rationale**: Leveraging existing Better Auth session management to inject user_id into API calls
**Alternatives considered**: Custom JWT handling, alternative auth providers
**Choice justified**: Consistent with existing authentication patterns in the project

#### Decision: Conversation State Management
**Rationale**: Using React component state to manage conversation_id rather than URL parameters for simplicity
**Alternatives considered**: URL parameters (?conversation_id=), localStorage, Redux
**Choice justified**: UI-only state that doesn't need persistence across sessions

#### Decision: Error Handling Strategy
**Rationale**: Explicit error messages to users rather than silent retries
**Alternatives considered**: Silent retries, generic error messages
**Choice justified**: Better user experience with transparency about connection issues

## Phase 1: Design & Contracts

### data-model.md

#### Conversation Entity
- **Fields**:
  - conversation_id (integer): Unique identifier returned by backend
  - user_id (string): Authenticated user identifier
  - created_at (timestamp): Conversation creation time
- **Relationships**: Owned by a single user

#### Message Entity (UI-only state)
- **Fields**:
  - role (string): "user" or "assistant"
  - content (string): Message text content
  - timestamp (timestamp): Message creation time
- **Validation**: Content must not be empty, role must be valid

### API Contracts

#### Frontend → Backend
**Endpoint**: POST /api/{user_id}/chat
**Request Body**:
```json
{
  "conversation_id": "integer (optional)",
  "message": "string (required)"
}
```
**Response Body**:
```json
{
  "conversation_id": "integer",
  "response": "string",
  "tool_calls": "array"
}
```

#### Authentication Header
**Required**: Authorization: Bearer {jwt_token}

### quickstart.md

#### Development Setup
1. Install ChatKit: `npm install @openai/chatkit`
2. Verify Better Auth integration is working
3. Test API endpoint connection at /api/{user_id}/chat
4. Start development server: `npm run dev`

#### Running the Chat Interface
1. Navigate to /chat route
2. Verify authentication is required
3. Test sending messages to backend
4. Verify conversation continuity

### Component Architecture

#### File Structure
```
/app
  /chat
    page.tsx          # Route and auth guard
/components
  /chat
    ChatProvider.tsx  # Conversation state
    ChatView.tsx      # ChatKit UI wrapper
/lib
  /chat
    api.ts           # API client for backend
```

#### Component Responsibilities
- **page.tsx**: Handle authentication guard and initial component mounting
- **ChatProvider**: Manage conversation_id and message state
- **ChatView**: Render ChatKit interface and handle user interactions
- **api.ts**: Handle API communication with backend endpoint

## Phase 2: Implementation Strategy

### Implementation Order
1. Set up basic Next.js page with auth guard
2. Integrate ChatKit UI components
3. Implement API client for backend communication
4. Connect auth session to inject user_id
5. Handle conversation_id lifecycle
6. Add loading and error states
7. Test conversation continuity

### Quality Assurance
- Unit tests for API client functions
- Integration test for auth flow
- Manual testing of conversation continuity
- Error handling verification
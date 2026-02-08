# Tasks: Authentication & API Security (Better Auth + JWT)

**Input**: Design documents from `/specs/002-auth-security-jwt/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Install Better Auth in frontend directory
- [x] T002 [P] Install JWT dependencies in backend requirements.txt
- [x] T003 Create shared secret environment variable configuration

---
## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Configure Better Auth with JWT plugin in frontend/lib/auth.js
- [x] T005 [P] Create JWT utility functions in backend/src/auth/jwt.py
- [x] T006 [P] Create auth dependencies in backend/src/auth/dependencies.py
- [x] T007 Update backend configuration with JWT settings in backend/src/core/config.py
- [x] T008 Create frontend API client with JWT injection in frontend/services/api-client.js
- [x] T009 Update backend main.py to include auth dependencies

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---
## Phase 3: User Story 1 - Authenticate User (Priority: P1) 🎯 MVP

**Goal**: Enable users to sign up and sign in to the application and receive JWT tokens

**Independent Test**: Can register a user, log in, and verify that a valid JWT token is issued that can be used for subsequent API requests

### Implementation for User Story 1

- [x] T010 [P] [US1] Create login component in frontend/components/auth/Login.jsx
- [x] T011 [P] [US1] Create signup component in frontend/components/auth/Signup.jsx
- [x] T012 [US1] Implement login page in frontend/pages/login.jsx
- [x] T013 [US1] Implement signup page in frontend/pages/signup.jsx
- [x] T014 [US1] Test user authentication flow manually

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---
## Phase 4: User Story 2 - Secure API Requests (Priority: P1)

**Goal**: Ensure all API requests are authenticated with JWT tokens and properly validated

**Independent Test**: Can make API requests with a valid JWT token and verify that only the authenticated user's tasks are returned, and that requests without tokens are rejected

### Implementation for User Story 2

- [x] T015 [P] [US2] Update existing task endpoints to require authentication in backend/src/api/v1/routes/tasks.py
- [x] T016 [US2] Implement JWT token verification in API requests
- [x] T017 [US2] Test authenticated vs unauthenticated API requests manually
- [x] T018 [US2] Verify proper error responses (401) for invalid tokens

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---
## Phase 5: User Story 3 - Enforce User Data Isolation (Priority: P2)

**Goal**: Ensure users can only access their own tasks by enforcing JWT user_id matches URL user_id

**Independent Test**: Create tasks for multiple users and verify that each user can only access their own tasks, even when attempting to access another user's data via the API

### Implementation for User Story 3

- [x] T019 [P] [US3] Update task service functions to enforce user_id matching in backend/src/services/task_service.py
- [x] T020 [US3] Implement user_id validation in task endpoints in backend/src/api/v1/routes/tasks.py
- [x] T021 [US3] Test cross-user access attempts (should fail)
- [x] T022 [US3] Verify proper error responses (403) for mismatched user_ids

**Checkpoint**: User Stories 1, 2, and 3 should all be independently functional

---
## Phase 6: User Story 4 - Handle Token Expiration (Priority: P2)

**Goal**: Properly handle expired JWT tokens and notify users when their session ends

**Independent Test**: Use an expired JWT token for API requests and verify that the system properly rejects these requests with appropriate error responses

### Implementation for User Story 4

- [x] T023 [P] [US4] Update JWT token expiration handling in backend/src/auth/jwt.py
- [x] T024 [US4] Implement token expiration validation in auth dependencies
- [x] T025 [US4] Test expired token handling manually
- [x] T026 [US4] Verify proper error responses (401) for expired tokens

**Checkpoint**: All user stories should now be independently functional

---
## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T027 [P] Update error handling for auth failures in backend/src/main.py
- [x] T028 [P] Add auth-specific logging for debugging purposes
- [x] T029 Update .env.example with auth-related environment variables
- [x] T030 Run end-to-end auth testing to validate all authentication flows work correctly
- [x] T031 Verify all security requirements from spec are implemented
- [x] T032 Test cross-user access prevention and token validation

---
## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1-US3 but should be independently testable

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---
## Parallel Example: User Story 1

```bash
# Launch all components for User Story 1 together:
Task: "Create login component in frontend/components/auth/Login.jsx"
Task: "Create signup component in frontend/components/auth/Signup.jsx"

# Launch all pages for User Story 1 together:
Task: "Implement login page in frontend/pages/login.jsx"
Task: "Implement signup page in frontend/pages/signup.jsx"
```

---
## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---
## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
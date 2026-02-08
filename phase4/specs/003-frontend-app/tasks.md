# Tasks: Frontend Application (Next.js + Better Auth)

**Input**: Design documents from `/specs/003-frontend-app/`
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

- [X] T001 Create frontend directory structure per plan.md
- [X] T002 [P] Initialize Next.js project with App Router in frontend/
- [X] T003 [P] Install Better Auth dependencies in frontend package.json
- [X] T004 [P] Install Tailwind CSS and configure for frontend/
- [X] T005 Create basic Next.js configuration files (next.config.js, tailwind.config.js)
- [X] T006 Create .env.example with required environment variables

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T007 Configure Better Auth client in frontend/src/lib/auth.js
- [X] T008 Create API client utility with JWT injection in frontend/src/services/api-client.js
- [X] T009 Create auth context and provider in frontend/src/contexts/auth-context.js
- [X] T010 Create useAuth hook in frontend/src/hooks/useAuth.js
- [X] T011 Create basic layout structure in frontend/src/app/layout.jsx
- [X] T012 Create protected route component for dashboard section

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration and Authentication (Priority: P1) 🎯 MVP

**Goal**: Enable users to sign up and sign in to the application and receive JWT tokens

**Independent Test**: Can register a user, log in, and verify that a valid JWT token is issued that can be used for subsequent API requests

### Implementation for User Story 1

- [X] T013 [P] [US1] Create LoginForm component in frontend/src/components/auth/LoginForm.jsx
- [X] T014 [P] [US1] Create SignupForm component in frontend/src/components/auth/SignupForm.jsx
- [X] T015 [P] [US1] Create auth page layout in frontend/src/app/(auth)/layout.jsx
- [X] T016 [US1] Implement login page in frontend/src/app/(auth)/login/page.jsx
- [X] T017 [US1] Implement signup page in frontend/src/app/(auth)/signup/page.jsx
- [X] T018 [US1] Test user authentication flow manually

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View and Manage Personal Tasks (Priority: P1)

**Goal**: Allow authenticated users to create, view, update, delete, and complete tasks

**Independent Test**: Can make API requests with a valid JWT token and verify that only the authenticated user's tasks are returned, and that requests without tokens are rejected

### Implementation for User Story 2

- [X] T019 [P] [US2] Create TaskList component in frontend/src/components/tasks/TaskList.jsx
- [X] T020 [P] [US2] Create TaskItem component in frontend/src/components/tasks/TaskItem.jsx
- [X] T021 [P] [US2] Create TaskForm component in frontend/src/components/tasks/TaskForm.jsx
- [X] T022 [P] [US2] Create useTasks hook in frontend/src/hooks/useTasks.js
- [X] T023 [US2] Implement dashboard layout in frontend/src/app/dashboard/layout.jsx
- [X] T024 [US2] Implement tasks page in frontend/src/app/dashboard/tasks/page.jsx
- [X] T025 [US2] Implement task creation form in frontend/src/app/dashboard/tasks/create/page.jsx
- [X] T026 [US2] Implement individual task page in frontend/src/app/dashboard/tasks/[id]/page.jsx
- [X] T027 [US2] Test authenticated task operations manually

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Responsive UI Experience Across Devices (Priority: P2)

**Goal**: Ensure the application layout and functionality work properly on different screen sizes

**Independent Test**: The application layout and functionality work properly on different screen sizes. UI elements resize, reposition, and adapt to accommodate various viewport dimensions while maintaining core functionality.

### Implementation for User Story 3

- [X] T028 [P] [US3] Add responsive styling to LoginForm component
- [X] T029 [P] [US3] Add responsive styling to SignupForm component
- [X] T030 [P] [US3] Add responsive styling to TaskList component
- [X] T031 [P] [US3] Add responsive styling to TaskItem component
- [X] T032 [P] [US3] Add responsive styling to TaskForm component
- [X] T033 [US3] Test responsive behavior across different screen sizes

**Checkpoint**: User Stories 1, 2, and 3 should all be independently functional

---

## Phase 6: User Story 4 - Error Handling and Loading States (Priority: P2)

**Goal**: Display appropriate loading indicators during API calls and clear error messages when operations fail

**Independent Test**: The application displays appropriate loading indicators during API calls and clear error messages when operations fail. Users understand the state of their requests at all times.

### Implementation for User Story 4

- [X] T034 [P] [US4] Add loading states to LoginForm component
- [X] T035 [P] [US4] Add error handling to LoginForm component
- [X] T036 [P] [US4] Add loading states to SignupForm component
- [X] T037 [P] [US4] Add error handling to SignupForm component
- [X] T038 [P] [US4] Add loading states to TaskList component
- [X] T039 [P] [US4] Add error handling to TaskList component
- [X] T040 [P] [US4] Add loading and error states to TaskForm component
- [X] T041 [US4] Implement empty state for TaskList when no tasks exist
- [X] T042 [US4] Test error handling and loading states manually

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T043 [P] Add global error boundary for the application
- [X] T044 [P] Add global loading indicator
- [X] T045 Update .env.example with all required environment variables
- [X] T046 Run end-to-end testing to validate all authentication and task management flows work correctly
- [X] T047 Verify all security requirements from spec are implemented
- [X] T048 Test responsive design and error handling across all components

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
Task: "Create LoginForm component in frontend/src/components/auth/LoginForm.jsx"
Task: "Create SignupForm component in frontend/src/components/auth/SignupForm.jsx"

# Launch all pages for User Story 1 together:
Task: "Implement login page in frontend/src/app/(auth)/login/page.jsx"
Task: "Implement signup page in frontend/src/app/(auth)/signup/page.jsx"
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
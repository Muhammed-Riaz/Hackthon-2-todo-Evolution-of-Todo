# Tasks: Backend Core & Data Layer (FastAPI + Neon PostgreSQL)

**Input**: Design documents from `/specs/001-backend-core-data/`
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

- [x] T001 Create project structure per implementation plan in backend/
- [x] T002 Initialize Python project with FastAPI, SQLModel, and database dependencies in backend/
- [x] T003 [P] Create requirements.txt with FastAPI, SQLModel, uvicorn, psycopg2-binary dependencies

---
## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Setup database connection and session management in backend/src/database/
- [x] T005 [P] Create configuration management with environment variables in backend/src/core/config.py
- [x] T006 [P] Create base SQLModel with common fields in backend/src/models/base.py
- [x] T007 Create Task model based on data model in backend/src/models/task_model.py
- [x] T008 Setup Alembic for database migrations in backend/alembic.ini
- [x] T009 Create Pydantic schemas for Task entity in backend/src/schemas/task_schemas.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---
## Phase 3: User Story 1 - Create Task (Priority: P1) 🎯 MVP

**Goal**: Enable users to create new tasks associated with their account

**Independent Test**: Can send a POST request to /api/{user_id}/tasks with task details and verify that the task is stored in the database and returned with a success response

### Implementation for User Story 1

- [x] T010 [P] [US1] Create TaskCreate schema in backend/src/schemas/task_schemas.py
- [x] T011 [US1] Create task service functions in backend/src/services/task_service.py
- [x] T012 [US1] Implement POST endpoint for creating tasks in backend/src/api/v1/routes/tasks.py
- [x] T013 [US1] Add validation for required fields in task creation
- [x] T014 [US1] Test task creation manually via API

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---
## Phase 4: User Story 2 - List User Tasks (Priority: P1)

**Goal**: Allow users to retrieve all tasks associated with their account

**Independent Test**: Can create multiple tasks for different users and verify that each user can only see their own tasks when requesting /api/{user_id}/tasks

### Implementation for User Story 2

- [x] T015 [P] [US2] Create query function to get tasks by user_id in backend/src/services/task_service.py
- [x] T016 [US2] Implement GET endpoint for listing tasks in backend/src/api/v1/routes/tasks.py
- [x] T017 [US2] Add user_id filtering to ensure proper data isolation
- [x] T018 [US2] Test task listing manually via API

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---
## Phase 5: User Story 3 - View Individual Task (Priority: P2)

**Goal**: Allow users to retrieve details of a specific task

**Independent Test**: Can create a task and then retrieve it by its ID to verify the details match

### Implementation for User Story 3

- [x] T019 [P] [US3] Create function to get specific task by ID in backend/src/services/task_service.py
- [x] T020 [US3] Implement GET endpoint for specific task in backend/src/api/v1/routes/tasks.py
- [x] T021 [US3] Add validation to ensure user can only access their own tasks
- [x] T022 [US3] Test individual task retrieval manually via API

**Checkpoint**: User Stories 1, 2, and 3 should all be independently functional

---
## Phase 6: User Story 4 - Update Task (Priority: P2)

**Goal**: Allow users to modify the details of a task

**Independent Test**: Can update a task and verify the changes are reflected when retrieving the task again

### Implementation for User Story 4

- [x] T023 [P] [US4] Create TaskUpdate schema in backend/src/schemas/task_schemas.py
- [x] T024 [US4] Create function to update task in backend/src/services/task_service.py
- [x] T025 [US4] Implement PUT endpoint for updating tasks in backend/src/api/v1/routes/tasks.py
- [x] T026 [US4] Add validation to ensure user can only update their own tasks
- [x] T027 [US4] Test task update manually via API

**Checkpoint**: User Stories 1-4 should all be independently functional

---
## Phase 7: User Story 5 - Complete Task (Priority: P3)

**Goal**: Allow users to mark a task as completed

**Independent Test**: Can mark a task as complete and verify the completion status is updated

### Implementation for User Story 5

- [x] T028 [P] [US5] Create function to toggle task completion in backend/src/services/task_service.py
- [x] T029 [US5] Implement PATCH endpoint for completing tasks in backend/src/api/v1/routes/tasks.py
- [x] T030 [US5] Add validation to ensure user can only complete their own tasks
- [x] T031 [US5] Test task completion manually via API

**Checkpoint**: User Stories 1-5 should all be independently functional

---
## Phase 8: User Story 6 - Delete Task (Priority: P2)

**Goal**: Allow users to remove tasks that they no longer need

**Independent Test**: Can delete a task and verify it no longer appears in the user's task list

### Implementation for User Story 6

- [x] T032 [P] [US6] Create function to delete task in backend/src/services/task_service.py
- [x] T033 [US6] Implement DELETE endpoint for deleting tasks in backend/src/api/v1/routes/tasks.py
- [x] T034 [US6] Add validation to ensure user can only delete their own tasks
- [x] T035 [US6] Test task deletion manually via API

**Checkpoint**: All user stories should now be independently functional

---
## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T036 [P] Add comprehensive error handling with proper HTTP status codes
- [x] T037 [P] Add request logging for debugging purposes
- [x] T038 Create main application file with all routes in backend/src/main.py
- [x] T039 Update .env.example with required environment variables
- [x] T040 Run manual API tests to validate all endpoints work correctly
- [x] T041 Verify all requirements from spec are implemented
- [x] T042 Test database persistence across server restarts

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
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1-US4 but should be independently testable
- **User Story 6 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1-US5 but should be independently testable

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
# Launch all models for User Story 1 together:
Task: "Create TaskCreate schema in backend/src/schemas/task_schemas.py"
Task: "Create task service functions in backend/src/services/task_service.py"

# Launch all implementation for User Story 1 together:
Task: "Implement POST endpoint for creating tasks in backend/src/api/v1/routes/tasks.py"
Task: "Add validation for required fields in task creation"
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
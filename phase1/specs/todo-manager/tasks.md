---
description: "Task list for Todo In-Memory Python Console App implementation"
---

# Tasks: Todo In-Memory Python Console App

**Input**: Design documents from `/specs/todo-manager/`
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

- [x] T001 Create project structure per implementation plan
- [x] T002 [P] Create src/ directory with __init__.py files
- [x] T003 [P] Create tests/ directory with __init__.py files

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Create Task data model in src/models.py
- [x] T005 Create TodoManager class in src/todo_manager.py (skeleton)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Task Creation (Priority: P1) 🎯 MVP

**Goal**: Implement core functionality to create and store tasks with validation

**Independent Test**: Verify that tasks can be created with auto-incremented IDs, titles, descriptions, and default completion status

### Implementation for User Story 1

- [x] T006 [P] [US1] Implement Task dataclass in src/models.py with id, title, description, completed fields
- [x] T007 [US1] Implement add_task method in TodoManager class in src/todo_manager.py
- [x] T008 [US1] Add validation for non-empty titles in add_task method
- [x] T009 [US1] Implement auto-incrementing ID functionality in TodoManager
- [x] T010 [US1] Add type hints and docstrings to all methods
- [x] T011 [US1] Test Task creation with auto-incremented IDs

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Task Retrieval (Priority: P2)

**Goal**: Implement functionality to retrieve tasks (all tasks and by ID)

**Independent Test**: Verify that all tasks can be retrieved and individual tasks can be retrieved by ID

### Implementation for User Story 2

- [x] T012 [P] [US2] Implement get_all_tasks method in TodoManager class in src/todo_manager.py
- [x] T013 [US2] Implement get_task_by_id method in TodoManager class in src/todo_manager.py
- [x] T014 [US2] Add proper return types (list[Task] and Task | None) to retrieval methods
- [x] T015 [US2] Add type hints and docstrings to retrieval methods
- [x] T016 [US2] Test retrieval functionality

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Task Update (Priority: P3)

**Goal**: Implement functionality to update existing tasks

**Independent Test**: Verify that tasks can be updated with new titles and descriptions while preserving other fields

### Implementation for User Story 3

- [x] T017 [US3] Implement update_task method in TodoManager class in src/todo_manager.py
- [x] T018 [US3] Add validation for non-empty titles in update_task method
- [x] T019 [US3] Ensure only provided fields are updated (not None values)
- [x] T020 [US3] Add type hints and docstrings to update_task method
- [x] T021 [US3] Test update functionality

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Task Deletion (Priority: P4)

**Goal**: Implement functionality to delete tasks by ID

**Independent Test**: Verify that tasks can be deleted and the method returns appropriate success status

### Implementation for User Story 4

- [x] T022 [US4] Implement delete_task method in TodoManager class in src/todo_manager.py
- [x] T023 [US4] Return boolean value indicating success/failure of deletion
- [x] T024 [US4] Add type hints and docstrings to delete_task method
- [x] T025 [US4] Test deletion functionality

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: User Story 5 - Task Completion Toggle (Priority: P5)

**Goal**: Implement functionality to toggle the completion status of tasks

**Independent Test**: Verify that task completion status can be toggled and the updated task is returned

### Implementation for User Story 5

- [x] T026 [US5] Implement toggle_complete method in TodoManager class in src/todo_manager.py
- [x] T027 [US5] Toggle completion status and return updated Task
- [x] T028 [US5] Add type hints and docstrings to toggle_complete method
- [x] T029 [US5] Test toggle functionality

**Checkpoint**: All user stories should now be complete and functional

---

## Phase 8: User Story 6 - Error Handling (Priority: P6)

**Goal**: Implement comprehensive error handling for all methods

**Independent Test**: Verify that invalid inputs are handled gracefully and appropriate error messages are returned

### Implementation for User Story 6

- [x] T030 [US6] Add ValueError raising for empty/whitespace-only titles
- [x] T031 [US6] Handle invalid task IDs gracefully (return None where appropriate)
- [x] T032 [US6] Add proper exception documentation in docstrings
- [x] T033 [US6] Test error handling functionality

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T034 [P] Create main.py as application entry point
- [x] T035 [P] Create README.md with usage instructions
- [x] T036 Code cleanup and refactoring across all modules
- [x] T037 [P] Add comprehensive docstrings to all classes and methods
- [x] T038 Run validation tests to ensure all functionality works correctly
- [x] T039 Update quickstart documentation

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
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - May integrate with US1-3 but should be independently testable
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - May integrate with US1-4 but should be independently testable
- **User Story 6 (P6)**: Can start after Foundational (Phase 2) - Integrates with all previous stories

### Within Each User Story

- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all parallel tasks for User Story 1 together:
Task: "Implement Task dataclass in src/models.py with id, title, description, completed fields"
Task: "Implement add_task method in TodoManager class in src/todo_manager.py"
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
   - Developer D: User Story 4
   - Developer E: User Story 5
   - Developer F: User Story 6
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
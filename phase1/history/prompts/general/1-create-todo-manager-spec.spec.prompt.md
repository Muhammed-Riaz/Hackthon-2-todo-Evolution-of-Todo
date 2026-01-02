---
id: 1
title: Create Todo Manager Spec
stage: spec
date: 2026-01-01
surface: agent
model: claude-sonnet-4-5-20250929
feature: todo-manager
branch: 1-physical-ai-textbook
user: user
command: /sp.specify
labels: [specification, todo-manager, models]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - specs/todo-manager/spec.md
tests:
 - null
---

## Prompt

```
/sp.speify Task Model and In-Memory Todo Manager

Target audience: Claude Code (as implementation generator) and future hackathon phases (web, database, AI agents)
Focus: Define a clean, reusable Task dataclass and an in-memory TodoManager class that handles all CRUD operations for tasks

Success criteria:
- A Task dataclass (or pydantic/SQLModel-compatible class) with fields: id (int, auto-incremented), title (str, required), description (str, optional), completed (bool, default False)
- A TodoManager class that maintains a private list of Task objects and provides methods:
  - add_task(title: str, description: str = "") -> Task
  - get_all_tasks() -> list[Task]
  - get_task_by_id(task_id: int) -> Task | None
  - update_task(task_id: int, title: str | None = None, description: str | None = None) -> Task | None
  - delete_task(task_id: int) -> bool
  - toggle_complete(task_id: int) -> Task | None
- All methods include proper type hints, docstrings, and raise meaningful exceptions (e.g., ValueError for invalid ID or empty title)
- ID generation is automatic, sequential, and starts from 1
- Code follows PEP 8, uses meaningful names, and is fully testable in isolation

Constraints:
- Implementation file: src/todo_manager.py (export TodoManager and Task)
- Separate models file: src/models.py (define Task class/dataclass)
- Use only Python standard library (no external dependencies like pydantic yet – keep it pure stdlib for Phase I)
- Task title must not be empty or whitespace-only (validation in add/update)
- All public methods must handle invalid inputs gracefully and return appropriate values
- Code must be 100% generated from this spec by Claude Code

Not building:
- Any CLI or user interface code
- Persistence to file/database
- Priority, tags, due dates, or any intermediate/advanced features
- Sorting, filtering, or searching logic
- Any integration with external APIs or AI agents
```

## Response snapshot

Created the specification file at `specs/todo-manager/spec.md` defining:
- Task data model with id (int, auto-incremented), title (str, required), description (str, optional), completed (bool, default False)
- TodoManager class with methods: add_task, get_all_tasks, get_task_by_id, update_task, delete_task, toggle_complete
- All requirements for type hints, validation, error handling, and PEP 8 compliance
- Clear acceptance criteria for implementation

## Outcome

- ✅ Impact: Created comprehensive specification for TodoManager and Task model
- 🧪 Tests: N/A
- 📁 Files: Created specs/todo-manager/spec.md
- 🔁 Next prompts: Can proceed with implementation based on this spec
- 🧠 Reflection: Specification provides clear requirements for both models.py and todo_manager.py files

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
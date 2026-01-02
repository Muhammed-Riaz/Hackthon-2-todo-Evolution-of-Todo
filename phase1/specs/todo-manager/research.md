# Research: Todo In-Memory Python Console App

## Decision: Task representation
**Rationale**: Dataclass chosen for clarity and future SQLModel compatibility while maintaining minimal dependencies. Dataclasses provide clean, readable code with built-in features like default values and type hints, making them ideal for the Task model. They're part of the Python standard library since 3.7, satisfying the "standard library only" constraint.

**Alternatives considered**:
- Simple class: More verbose, requires manual implementation of `__init__`, `__repr__`, etc.
- Named tuple: Immutable by default, which could limit future functionality for updates
- Pydantic models: More feature-rich but would require external dependency

## Decision: TodoManager design
**Rationale**: Instantiable class chosen over singleton for better testability and future multi-user extensions. While a singleton would provide simplicity for a single-user console app, an instantiable class allows for better testing isolation and provides a clear path for future multi-user extensions without major refactoring.

**Alternatives considered**:
- Singleton pattern: Simpler for single-user application but harder to test
- Static methods: Would make state management more complex

## Decision: CLI style
**Rationale**: Command-based interface chosen over menu-driven for better UX while keeping implementation simple. Command-based interfaces are more intuitive for command-line applications and allow for faster interaction without navigating menus. Commands like "add Buy milk" are natural and user-friendly.

**Alternatives considered**:
- Menu-driven (numbered options): More guided but slower for frequent use
- Mixed approach: Could be confusing for users

## Decision: Error handling strategy
**Rationale**: Print friendly messages and continue loop chosen for user-friendliness. This approach provides immediate feedback to users without crashing the application, maintaining the console session. Debuggability is maintained through clear error messages that indicate the problem.

**Alternatives considered**:
- Raise exceptions: Could crash the application, disrupting user workflow
- Silent failures: Would confuse users without feedback

## Decision: Output formatting for list command
**Rationale**: Pretty-printed with status icons (✔/✖) chosen to balance readability and minimalism. Visual indicators make it easy to identify completed tasks at a glance while maintaining clean formatting. This provides better UX than simple text table.

**Alternatives considered**:
- Simple text table: Less visually appealing
- JSON output: Not user-friendly for console application
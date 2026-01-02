# Quickstart: Todo In-Memory Python Console App

## Getting Started

The Todo In-Memory Python Console App is a simple command-line application that allows users to manage their tasks. The application stores tasks in memory and provides basic CRUD operations.

## Prerequisites

- Python 3.13 or higher
- No external dependencies required (uses only standard library)

## Project Structure

```
src/
├── models.py        # Task data model
├── todo_manager.py  # TodoManager business logic
├── main.py         # Application entry point with CLI interface
└── __init__.py      # Package initialization
```

## Basic Usage

1. **Run the application**:
   ```bash
   python -m src.main
   ```

2. **Available commands**:
   - `add` - Add a new task
   - `list` - List all tasks
   - `update` - Update a task by ID
   - `delete` - Delete a task by ID
   - `complete` - Toggle completion status of a task
   - `exit` - Exit the application

## Example Workflow

```
Welcome to the Todo Console App!
Commands: add, list, update, delete, complete, exit

Enter command: add
Enter task title: Buy groceries
Enter task description (optional): Milk, bread, eggs
Added task #1: Buy groceries

Enter command: add
Enter task title: Walk the dog
Added task #2: Walk the dog

Enter command: list
1. [○] Buy groceries - Milk, bread, eggs
2. [○] Walk the dog -

Enter command: complete
Enter task ID to toggle completion: 1
Task #1 marked as completed

Enter command: list
1. [✓] Buy groceries - Milk, bread, eggs
2. [○] Walk the dog -

Enter command: exit
Goodbye!
```

## Development

To extend the application:

1. Modify the Task model in `src/models.py` if additional fields are needed
2. Add new functionality to `TodoManager` in `src/todo_manager.py`
3. Update the main application loop in `src/main.py` if needed

## Testing

Run individual tests for each user story:
- `python test_us1.py` - Test task creation
- `python test_us2.py` - Test task retrieval
- `python test_us3.py` - Test task update
- `python test_us4.py` - Test task deletion
- `python test_us5.py` - Test task completion toggle
- `python test_us6.py` - Test error handling
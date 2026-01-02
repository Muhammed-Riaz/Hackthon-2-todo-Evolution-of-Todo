# Todo In-Memory Python Console App

A simple, in-memory todo console application that allows users to manage their tasks with basic CRUD operations.

## Features

- Add tasks with titles and descriptions
- List all tasks with completion status
- Update task titles and descriptions
- Delete tasks by ID
- Toggle task completion status
- Input validation and error handling

## Requirements

- Python 3.13 or higher

## Usage

To run the application:

```bash
python -m src.main
```

### Available Commands

- `add`: Add a new task
- `list`: List all tasks
- `update`: Update a task by ID
- `delete`: Delete a task by ID
- `complete`: Toggle completion status of a task
- `exit`: Exit the application

### Example Workflow

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

## Architecture

The application follows a clean architecture pattern:

- `src/models.py`: Contains the Task data model
- `src/todo_manager.py`: Contains the TodoManager business logic
- `src/main.py`: Application entry point with CLI interface
- `specs/`: Contains specification documents for the project

## Implementation Details

- All task data is stored in-memory only (data is lost on exit)
- Tasks have auto-incremented IDs, titles, descriptions, and completion status
- All operations include proper validation and error handling
- The application uses only Python standard library (no external dependencies)

## Development

The application was developed following the Spec-Driven Development approach, with comprehensive specifications, plans, and task breakdowns in the `specs/` directory.

### Running Tests

The following test scripts are available to verify each user story:

- `python test_us1.py` - Test task creation
- `python test_us2.py` - Test task retrieval
- `python test_us3.py` - Test task update
- `python test_us4.py` - Test task deletion
- `python test_us5.py` - Test task completion toggle
- `python test_us6.py` - Test error handling
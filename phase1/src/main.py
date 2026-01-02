"""Main entry point for the Todo In-Memory Python Console App."""

from .todo_manager import TodoManager
from .models import Task


def main():
    """Run the main application loop."""
    print("Welcome to the Todo Console App!")
    print("Commands: add, list, update, delete, complete, exit")

    manager = TodoManager()

    while True:
        try:
            command = input("\nEnter command: ").strip().lower()

            if command == "exit":
                print("Goodbye!")
                break
            elif command == "add":
                title = input("Enter task title: ").strip()
                description = input("Enter task description (optional): ").strip()
                if not description:
                    description = ""

                try:
                    task = manager.add_task(title, description)
                    print(f"Added task #{task.id}: {task.title}")
                except ValueError as e:
                    print(f"Error: {e}")
            elif command == "list":
                tasks = manager.get_all_tasks()
                if not tasks:
                    print("No tasks found.")
                else:
                    for task in tasks:
                        status = "✓" if task.completed else "○"
                        print(f"{task.id}. [{status}] {task.title} - {task.description}")
            elif command == "update":
                try:
                    task_id = int(input("Enter task ID to update: "))
                    current_task = manager.get_task_by_id(task_id)
                    if current_task is None:
                        print(f"Task with ID {task_id} not found.")
                        continue

                    new_title = input(f"Enter new title (current: '{current_task.title}'): ").strip()
                    new_description = input(f"Enter new description (current: '{current_task.description}'): ").strip()

                    # Use None if the user didn't provide a new value
                    title_to_update = new_title if new_title else None
                    description_to_update = new_description if new_description else None

                    updated_task = manager.update_task(task_id, title_to_update, description_to_update)
                    if updated_task:
                        print(f"Updated task #{updated_task.id}: {updated_task.title}")
                    else:
                        print(f"Failed to update task with ID {task_id}")
                except ValueError:
                    print("Please enter a valid task ID (number).")
            elif command == "delete":
                try:
                    task_id = int(input("Enter task ID to delete: "))
                    success = manager.delete_task(task_id)
                    if success:
                        print(f"Deleted task with ID {task_id}")
                    else:
                        print(f"Task with ID {task_id} not found.")
                except ValueError:
                    print("Please enter a valid task ID (number).")
            elif command == "complete":
                try:
                    task_id = int(input("Enter task ID to toggle completion: "))
                    task = manager.toggle_complete(task_id)
                    if task:
                        status = "completed" if task.completed else "incomplete"
                        print(f"Task #{task.id} marked as {status}")
                    else:
                        print(f"Task with ID {task_id} not found.")
                except ValueError:
                    print("Please enter a valid task ID (number).")
            else:
                print("Unknown command. Available commands: add, list, update, delete, complete, exit")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
import argparse
import json
import os
from datetime import datetime
from typing import Dict, List, Optional

from regex import D
from tabulate import tabulate  # type: ignore

FILENAME = "tasks.json"
DATE_FORMAT = "%d-%m-%Y %H:%M"


def get_current_date() -> str:
    """
    Retrieves the current date formatted as a string.
    The date is returned in a predefined format specified by DATE_FORMAT.

    This function uses the current date and time to generate a string representation
    formatted according to the specified DATE_FORMAT. It is useful for timestamping tasks or events.

    Args:
        None

    Returns:
        str: The current date as a formatted string.
    """

    return datetime.now().strftime(DATE_FORMAT)


def initialize_task_file(filename: str = FILENAME) -> None:
    """
    Initializes the task file by creating it if it does not already exist.
    The task file is created as an empty JSON array, and the filename can be specified.

    This function checks for the existence of the specified filename.
    If the file does not exist, it creates the file and initializes it with an empty JSON array.

    Args:
        filename (str): The name of the file to initialize. Defaults to FILENAME.

    Returns:
        None
    """

    if not os.path.exists(filename):
        with open(filename, "w") as file:
            json.dump([], file)


def read_tasks(filename: str = FILENAME) -> List[Dict]:
    """
    Reads and returns the list of tasks from the specified task file.
    The tasks are expected to be in JSON format and returned as a list of dictionaries.

    This function checks for the existence of the specified filename and raises an error if the file is not found.
    It attempts to load the contents of the file, ensuring that the data is a valid list.
    If the file is corrupted or contains invalid JSON, appropriate exceptions are raised.

    Args:
        filename (str): The name of the file to read tasks from. Defaults to FILENAME.

    Returns:
        List[Dict]: A list of tasks loaded from the task file.

    Raises:
        FileNotFoundError: If the task file does not exist.
        ValueError: If the file content is not a valid list or contains invalid JSON.
    """

    if not os.path.exists(filename):
        raise FileNotFoundError(f"Task file '{filename}' not found.")

    with open(filename, "r") as file:
        try:
            tasks = json.load(file)
            if not isinstance(tasks, list):
                raise ValueError("Tasks file is corrupted or in an ivalid format.")
            return tasks
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Tasks file '{filename}' is corrupted or contains invalid JSON."
            ) from e


def write_tasks(tasks: List[Dict], filename: str = FILENAME) -> None:
    """
    Writes the provided list of tasks to the specified task file in JSON format.
    The tasks are saved with indentation for improved readability.

    This function opens the specified filename in write mode and serializes the given list of tasks into JSON format.
    It overwrites any existing content in the file with the new task data.

    Args:
        tasks (List[Dict]): A list of tasks to be written to the task file.
        filename (str): The name of the file to write tasks to. Defaults to FILENAME.

    Returns:
        None
    """

    with open(filename, "w") as file:
        json.dump(tasks, file, indent=4)


def add_task(description: str, filename: str = FILENAME) -> None:
    """
    Adds a new task with the specified description to the task list.
    If the task file does not exist, it initializes a new task file before adding the task.

    This function attempts to read the current list of tasks from the specified file.
    If the file is not found, it creates a new task file. A new task is then created with a unique ID,
    default status, and timestamps, and is appended to the task list. Finally, the updated task list is saved back to the file.

    Args:
        description (str): A brief description of the task to be added.
        filename (str): The name of the file to write tasks to. Defaults to FILENAME.

    Returns:
        None
    """

    try:
        tasks = read_tasks(filename)
    except FileNotFoundError:
        print(f"Task file '{filename}' not found. Initializing a new task file.")
        initialize_task_file(filename)
        tasks = []

    task = {
        "id": len(tasks) + 1,
        "description": description,
        "status": "todo",
        "createdAt": get_current_date(),
        "updatedAt": get_current_date(),
    }
    tasks.append(task)
    write_tasks(tasks, filename)
    print(f"Task added successfully (ID: {task['id']})")


def list_tasks(status: Optional[str] = None, filename: str = FILENAME) -> None:
    """
    Lists all tasks, optionally filtered by their status, from the specified task file.
    The tasks are displayed in a formatted table for easy viewing.

    This function attempts to read the current list of tasks from the specified file.
    If the file cannot be read due to errors, an appropriate message is displayed.
    If a status is provided, it filters the tasks accordingly.
    The tasks are then printed in a grid format, showing relevant details such as ID, description, status, and timestamps.
    If no tasks are found, a message is displayed indicating this.

    Args:
        status (Optional[str], optional): The status to filter tasks by (e.g., "todo", "done"). Defaults to None.
        filename (str): The name of the file to read tasks from. Defaults to FILENAME.

    Returns:
        None
    """

    try:
        tasks = read_tasks(filename)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error reading tasks: {e}")
        return

    if status:
        tasks = [task for task in tasks if task["status"] == status]

    if not tasks:
        print("No tasks found.")
        return

    table = [
        [
            task["id"],
            task["description"],
            task["status"],
            task["createdAt"],
            task["updatedAt"],
        ]
        for task in tasks
    ]

    headers = ["ID", "Description", "Status", "Created At", "Updated At"]
    print(tabulate(table, headers, tablefmt="grid"))


def update_task(task_id: int, new_description: str, filename: str = FILENAME) -> None:
    """
    Updates the description of an existing task identified by its ID in the specified task file.
    The task's updated timestamp is also modified to reflect the change.

    This function attempts to read the current list of tasks from the specified file.
    If the file cannot be read due to errors, an appropriate message is displayed.
    The function searches for a task with the specified ID, and if found, updates its description and timestamp.
    If the task ID does not exist, a message is printed indicating that the task was not found.

    Args:
        task_id (int): The ID of the task to be updated.
        new_description (str): The new description for the task.
        filename (str): The name of the file to read and write tasks. Defaults to FILENAME.

    Returns:
        None
    """

    try:
        tasks = read_tasks(filename)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error reading tasks: {e}")
        return

    for task in tasks:
        if task["id"] == task_id:
            task["description"] = new_description
            task["updatedAt"] = get_current_date()
            write_tasks(tasks, filename)
            print(f"Task {task_id} updated successfully.")
            return

    print(f"Task with ID {task_id} not found.")


def delete_task(task_id: int, filename: str = FILENAME) -> None:
    """
    Deletes a task identified by its ID from the specified task file.
    If the task ID does not exist, a message is displayed indicating that the task was not found.

    This function attempts to read the current list of tasks from the specified file.
    If the file cannot be read due to errors, an appropriate message is displayed.
    The function creates a new list of tasks excluding the task with the specified ID.
    If no tasks are removed, it indicates that the task was not found; otherwise, it saves the updated task list back to the file.

    Args:
        task_id (int): The ID of the task to be deleted.
        filename (str): The name of the file to read and write tasks. Defaults to FILENAME.

    Returns:
        None
    """

    try:
        tasks = read_tasks(filename)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error reading tasks: {e}")
        return

    new_tasks = [task for task in tasks if task["id"] != task_id]

    if len(new_tasks) == len(tasks):
        print(f"Task with ID {task_id} not found.")
        return
    write_tasks(new_tasks, filename)
    print(f"Task {task_id} deleted successfully.")


def mark_task(task_id: int, status: str, filename: str = FILENAME) -> None:
    """
    Marks a task identified by its ID with a specified status in the task file.
    The task's updated timestamp is also modified to reflect the change.

    This function attempts to read the current list of tasks from the specified file.
    If the file cannot be read due to errors, an appropriate message is displayed.
    The function searches for a task with the specified ID, and if found, updates its status and timestamp.
    If the task ID does not exist, a message is printed indicating that the task was not found.

    Args:
        task_id (int): The ID of the task to be marked.
        status (str): The new status to assign to the task.
        filename (str): The name of the file to read and write tasks. Defaults to FILENAME.

    Returns:
        None
    """

    try:
        tasks = read_tasks(filename)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error reading tasks: {e}")
        return
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            task["updatedAt"] = get_current_date()
            write_tasks(tasks, filename)
            print(f"Task {task_id} marked as {status}.")
            return

    print(f"Task with ID {task_id} not found.")


def main() -> None:
    """
    Main entry point for the Task Tracker command-line interface (CLI).
    This function initializes the task file and processes user commands to manage tasks.

    The function sets up an argument parser to handle various commands such as adding, listing, updating, deleting, and marking tasks.
    It validates the input and calls the appropriate functions based on the user's command and provided task information.
    Error messages are displayed for invalid inputs or missing information.

    Args:
        None

    Returns:
        None

    Examples:
        To add a task: `python task_cli.py add "New Task"`
        To list all tasks: `python task_cli.py list`

    """

    initialize_task_file()

    parser = argparse.ArgumentParser(description="Task Tracker CLI")
    parser.add_argument(
        "command",
        choices=["add", "list", "update", "delete", "mark-in-progress", "mark-done"],
        help="Action to perform",
    )
    parser.add_argument(
        "task_info",
        help="Description of the task or task ID",
        nargs="?",
        default=None,
    )

    args = parser.parse_args()

    command = args.command
    task_info = args.task_info
    # extra = args.extra

    if command == "add":
        if task_info:
            add_task(task_info)
        else:
            print("Error: Missing task description for 'add' command.")

    elif command == "list":
        list_tasks(status=task_info)

    elif command == "update":
        if task_info:
            try:
                task_id = int(task_info)
                update_task(task_id)
            except ValueError:
                print("Error: Task ID must be an integer.")
        else:
            print("Error: Missing task ID or new description for 'update' command.")

    elif command == "delete":
        if task_info:
            try:
                task_id = int(task_info)
                delete_task(task_id)
            except ValueError:
                print("Error: Task ID must be an integer.")
        else:
            print("Error: Missing task ID for 'delete' command.")

    elif command in ["mark-in-progress", "mark-done"]:
        if task_info:
            try:
                task_id = int(task_info)
                status = "in-progress" if command == "mark-in-progress" else "done"
                mark_task(task_id, status)
            except ValueError:
                print("Error: Task ID must be an integer.")
        else:
            print(f"Error: Missing task ID for '{command}' command.")
    else:
        print("Invalid command or arguments.")


if __name__ == "__main__":
    main()

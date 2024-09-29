import argparse
import json
import os
from datetime import datetime

from tabulate import tabulate  # type: ignore

FILENAME = "tasks.json"

current_format = "%d-%m-%Y %H:%M"
current_date = datetime.now().strftime(current_format)


def initialize_task_file() -> None:
    """
    Initializes the task file by creating it if it does not already exist.
    The task file is created as an empty JSON array.

    This function checks for the existence of a predefined filename.
    If the file does not exist, it creates the file and initializes it with an empty JSON array.

    Args:
        None

    Returns:
        None
    """

    if not os.path.exists(FILENAME):
        with open(FILENAME, "w") as file:
            json.dump([], file)


def read_tasks() -> list[dict]:
    """
    Reads and returns the list of tasks from the task file.
    The tasks are loaded from a JSON formatted file.

    This function opens the predefined task file in read mode and loads its contents as a Python object.
    It expects the file to contain a valid JSON array representing the tasks.

    Args:
        None

    Returns:
        list: A list of tasks loaded from the task file.

    Raises:
        FileNotFoundError: If the task file does not exist.
        json.JSONDecodeError: If the file content is not valid JSON.
    """

    with open(FILENAME, "r") as file:
        return json.load(file)


def write_tasks(tasks: list[dict]) -> None:
    """
    Writes the provided list of tasks to the task file.
    The tasks are saved in a JSON format with indentation for readability.

    This function opens the predefined task file in write mode and serializes the given list of tasks into JSON format.
    It overwrites any existing content in the file with the new task data.

    Args:
        tasks (list): A list of tasks to be written to the task file.

    Returns:
        None
    """

    with open(FILENAME, "w") as file:
        json.dump(tasks, file, indent=4)


def add_task(description: str) -> None:
    """
    Adds a new task with the specified description to the task list.
    The task is assigned a unique ID and initialized with a default status and timestamps.

    This function reads the current list of tasks, generates a new task object with a unique ID, and appends it to the list.
    After updating the task list, it writes the modified list back to the task file and confirms the addition of the task.

    Args:
        description (str): A brief description of the task to be added.

    Returns:
        None
    """

    tasks = read_tasks()
    task_id = len(tasks) + 1
    task = {
        "id": task_id,
        "description": description,
        "status": "todo",
        "createdAt": current_date,
        "updatedAt": current_date,
    }
    tasks.append(task)
    write_tasks(tasks)
    print(f"Task added successfully (ID: {task_id})")


def list_tasks(status=None) -> None:
    """
    Lists all tasks, optionally filtered by their status.
    The tasks are displayed in a formatted table for easy viewing.

    This function retrieves the current list of tasks and, if a status is provided, filters the tasks accordingly.
    It then prints the tasks in a grid format, showing relevant details such as ID, description, status, and timestamps.
    If no tasks are found, a message is displayed indicating this.

    Args:
        status (str, optional): The status to filter tasks by (e.g., "todo", "done"). Defaults to None.

    Returns:
        None
    """

    tasks = read_tasks()
    if status:
        tasks = [task for task in tasks if task["status"] == status]

    if not tasks:
        print("No tasks found.")
    else:
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


def update_task(task_id: int, new_description: str) -> None:
    """
    Updates the description of an existing task identified by its ID.
    The task's updated timestamp is also modified to reflect the change.

    This function retrieves the current list of tasks and searches for a task with the specified ID.
    If found, it updates the task's description and the timestamp, then saves the changes back to the task file.
    If the task ID does not exist, a message is printed indicating that the task was not found.

    Args:
        task_id (int): The ID of the task to be updated.
        new_description (str): The new description for the task.

    Returns:
        None
    """

    tasks = read_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = new_description
            task["updatedAt"] = current_date
            write_tasks(tasks)
            print(f"Task {task_id} updated successfully.")
            return
    print(f"Task with ID {task_id} not found.")


# Función para eliminar una tarea
def delete_task(task_id):
    tasks = read_tasks()
    tasks = [task for task in tasks if task["id"] != task_id]
    write_tasks(tasks)
    print(f"Task {task_id} deleted successfully.")


# Función para marcar una tarea como 'in-progress' o 'done'
def mark_task(task_id, status):
    tasks = read_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            task["updatedAt"] = current_date
            write_tasks(tasks)
            print(f"Task {task_id} marked as {status}.")
            return
    print(f"Task with ID {task_id} not found.")


# Función principal
def main():
    """
    Main function for the Task Tracker Command Line Interface (CLI).

    This function initializes the task file if it does not exist and sets up the argument parser to handle various commands related to task management. It processes user input to perform actions such as adding, listing, updating, deleting, and marking tasks.

    Args:
        command (str): The action to perform, which can be one of the following:
            "add", "list", "update", "delete", "mark-in-progress", or "mark-done".
        description_or_id (str, optional): The description of the task to add or the ID of the task to update, delete, or mark.
        extra (str, optional): Additional information for updating a task, such as a new description.

    Returns:
        None

    Raises:
        SystemExit: If the command is invalid or required arguments are missing.

    Examples:
        To add a task: `python task_cli.py add "New Task"`
        To list all tasks: `python task_cli.py list`
    """

    # Inicializa el archivo de tareas si no existe
    initialize_task_file()

    # Configura el manejo de argumentos
    parser = argparse.ArgumentParser(description="Task Tracker CLI")
    parser.add_argument(
        "command",
        choices=["add", "list", "update", "delete", "mark-in-progress", "mark-done"],
        help="Action to perform",
    )
    parser.add_argument(
        "description_or_id", help="Description of the task or task ID", nargs="?"
    )
    parser.add_argument(
        "extra", help="Additional info (e.g., new description)", nargs="?"
    )

    args = parser.parse_args()

    # Manejo de los diferentes comandos
    if args.command == "add" and args.description_or_id:
        add_task(args.description_or_id)

    elif args.command == "list":
        if args.description_or_id:
            list_tasks(
                args.description_or_id
            )  # Filtrar por estado (done, todo, in-progress)
        else:
            list_tasks()  # Listar todas las tareas

    elif args.command == "update" and args.description_or_id and args.extra:
        update_task(int(args.description_or_id), args.extra)

    elif args.command == "delete" and args.description_or_id:
        delete_task(int(args.description_or_id))

    elif args.command == "mark-in-progress" and args.description_or_id:
        mark_task(int(args.description_or_id), "in-progress")

    elif args.command == "mark-done" and args.description_or_id:
        mark_task(int(args.description_or_id), "done")

    else:
        print("Invalid command or missing arguments.")


if __name__ == "__main__":
    main()

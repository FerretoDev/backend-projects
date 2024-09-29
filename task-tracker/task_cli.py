import argparse
import json
import os
from datetime import datetime

from tabulate import tabulate  # type: ignore

FILENAME = "tasks.json"

current_format = "%d-%m-%Y %H:%M"
current_date = datetime.now().strftime(current_format)


# Función para inicializar el archivo JSON si no existe
def initialize_task_file():
    if not os.path.exists(FILENAME):
        with open(FILENAME, "w") as file:
            json.dump([], file)


# Función para leer las tareas
def read_tasks():
    with open(FILENAME, "r") as file:
        return json.load(file)


# Función para escribir tareas
def write_tasks(tasks):
    with open(FILENAME, "w") as file:
        json.dump(tasks, file, indent=4)


# Función para agregar una tarea
def add_task(description):

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


# Función para listar todas las tareas
def list_tasks(status=None):
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


# Función para actualizar una tarea
def update_task(task_id, new_description):
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


# Ejecuta la función main() si se llama directamente el script
if __name__ == "__main__":
    main()

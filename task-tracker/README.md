# Task Tracker CLI

---

A simple command line (CLI) based task manager that allows you to perform operations like (Create, Read, Update, Delete) on a list of tasks. Tasks are saved in a JSON file for persistence.

## Features

- **Add tasks**: Allows adding new tasks with a description and an initial `todo` status.
- **List tasks**: Displays all tasks or filters by their status (e.g., `todo`, `in-progress`, `done`).
- **Update tasks**: Allows changing the description of a task.
- **Delete tasks**: Deletes a task from the list.
- **Mark tasks**: Changes the status of a task to `in-progress` or `done`.

## Requirements

- Python 3.7 or higher
- Additional libraries: `tabulate`, `argparse`

### Installation

1. Clone the repository or download the files:

    ```bash
    git clone https://github.com/FerretoDev/backend-projects.git
    cd backend-projects/task-tracker
    ```

2. Install the necessary dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

The task manager runs from the command line. You must provide one of the available commands (`add`, `list`, `update`, `delete`, `mark-in-progress`, `mark-done`) followed by the necessary arguments.

### Add a Task

```bash
python task_cli.py add "New task"
```

This will add a new task with the initial `todo` status.

### List Tasks

To list all tasks:

```bash
python task_cli.py list
```

To list tasks filtered by status (e.g., `todo`, `in-progress`, `done`):

```bash
python task_cli.py list todo
```

### Update a Task

```bash
python task_cli.py update <task_id> "Updated description"
```

This will update the description of the task with the provided ID.

### Delete a Task

```bash
python task_cli.py delete <task_id>
```

This will delete the task with the provided ID.

### Mark a Task as `in-progress` or `done`

To mark a task as in progress:

```bash
python task_cli.py mark-in-progress <task_id>
```

To mark a task as completed:

```bash
python task_cli.py mark-done <task_id>
```

## Error Handling

- If you attempt to access or modify a task that doesn’t exist, an error message will be shown.
- If the task file is corrupt or has an invalid format, appropriate exceptions will be raised.

## Project Structure

- **task_cli.py**: Contains the main code for the task manager.
- **tasks.json**: File where tasks are stored in JSON format (automatically generated).
  
## Examples

### Adding and Listing Tasks:

```bash
$ python task_cli.py add "Buy milk"
Task added successfully (ID: 1)

$ python task_cli.py list
+----+----------------+---------+---------------------+---------------------+
| ID | Description    | Status  | Created At          | Updated At          |
+----+----------------+---------+---------------------+---------------------+
|  1 | Buy milk       | todo    | 29-09-2024 15:30    | 29-09-2024 15:30    |
+----+----------------+---------+---------------------+---------------------+
```

### Marking a Task as Completed:

```bash
$ python task_cli.py mark-done 1
Task 1 marked as done.

$ python task_cli.py list
+----+----------------+---------+---------------------+---------------------+
| ID | Description    | Status  | Created At          | Updated At          |
+----+----------------+---------+---------------------+---------------------+
|  1 | Buy milk       | done    | 29-09-2024 15:30    | 29-09-2024 15:32    |
+----+----------------+---------+---------------------+---------------------+
```


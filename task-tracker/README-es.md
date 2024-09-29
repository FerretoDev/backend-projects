# Task Tracker CLI

---

Un sencillo gestor de tareas basado en línea de comandos (CLI) que permite realizar operaciones como (Crear, Leer, Actualizar, Eliminar) sobre una lista de tareas. Las tareas se guardan en un archivo JSON para su persistencia.

## Funcionalidades

- **Añadir tareas**: Permite agregar nuevas tareas con descripción y estado inicial `todo`.
- **Listar tareas**: Muestra todas las tareas o filtra por su estado (e.g., `todo`, `in-progress`, `done`).
- **Actualizar tareas**: Permite cambiar la descripción de una tarea.
- **Eliminar tareas**: Elimina una tarea de la lista.
- **Marcar tareas**: Cambia el estado de una tarea a `in-progress` o `done`.

## Requisitos

- Python 3.7 o superior
- Librerías adicionales: `tabulate`, `argparse`

### Instalación

1. Clona el repositorio o descarga los archivos:

    ```bash
    git clone https://github.com/FerretoDev/backend-projects.git
    cd backend-projects/task-tracker
    ```

2. Instala las dependencias necesarias:

    ```bash
    pip install -r requirements.txt
    ```

## Uso

El gestor de tareas se ejecuta desde la línea de comandos. Debes proporcionar uno de los comandos disponibles (`add`, `list`, `update`, `delete`, `mark-in-progress`, `mark-done`) seguido de los argumentos necesarios.

### Añadir una tarea

```bash
python task_cli.py add "Nueva tarea"
```

Esto añadirá una nueva tarea con el estado inicial `todo`.

### Listar tareas

Para listar todas las tareas:

```bash
python task_cli.py list
```

Para listar tareas filtradas por estado (e.g., `todo`, `in-progress`, `done`):

```bash
python task_cli.py list todo
```

### Actualizar una tarea

```bash
python task_cli.py update <task_id> "Descripción actualizada"
```

Esto actualizará la descripción de la tarea con el ID proporcionado.

### Eliminar una tarea

```bash
python task_cli.py delete <task_id>
```

Esto eliminará la tarea con el ID proporcionado.

### Marcar una tarea como `in-progress` o `done`

Para marcar una tarea como en progreso:

```bash
python task_cli.py mark-in-progress <task_id>
```

Para marcar una tarea como completada:

```bash
python task_cli.py mark-done <task_id>
```

## Manejo de Errores

- Si intentas acceder o modificar una tarea que no existe, se mostrará un mensaje de error.
- Si el archivo de tareas está corrupto o tiene formato inválido, se lanzará una excepción apropiada.

## Estructura del Proyecto

- **task_cli.py**: Contiene el código principal del gestor de tareas.
- **tasks.json**: Archivo donde se guardan las tareas en formato JSON (se genera automáticamente).
  
## Ejemplos

### Añadir y listar tareas:

```bash
$ python task_cli.py add "Comprar leche"
Task added successfully (ID: 1)

$ python task_cli.py list
+----+----------------+---------+---------------------+---------------------+
| ID | Description    | Status  | Created At          | Updated At          |
+----+----------------+---------+---------------------+---------------------+
|  1 | Comprar leche  | todo    | 29-09-2024 15:30    | 29-09-2024 15:30    |
+----+----------------+---------+---------------------+---------------------+
```

### Marcar tarea como completada:

```bash
$ python task_cli.py mark-done 1
Task 1 marked as done.

$ python task_cli.py list
+----+----------------+---------+---------------------+---------------------+
| ID | Description    | Status  | Created At          | Updated At          |
+----+----------------+---------+---------------------+---------------------+
|  1 | Comprar leche  | done    | 29-09-2024 15:30    | 29-09-2024 15:32    |
+----+----------------+---------+---------------------+---------------------+
```

---

Este `README-es.md` proporciona una guía clara y directa sobre cómo usar el gestor de tareas, incluyendo ejemplos.
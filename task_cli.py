import sys
import json
import os
from datetime import datetime
from tabulate import tabulate
from argparse import ArgumentParser
from pathlib import Path
from typing import Callable

FILE = "tasks.json"
VALID_STATUS = ["todo", "progress", "done"]


# ---------- Utility ----------
def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def load_tasks():
    if not os.path.exists(FILE):
        return []

    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_tasks(tasks):
    with open(FILE, "w") as f:
        json.dump(tasks, f, indent=4)


def get_next_id(tasks):
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


# ---------- Core Features ----------
def add_task(description):
    if not description.strip():
        print("❌ Description cannot be empty")
        return

    tasks = load_tasks()

    task = {
        "id": get_next_id(tasks),
        "description": description,
        "status": "todo",
        "createdAt": now(),
        "updatedAt": now()
    }

    tasks.append(task)
    save_tasks(tasks)
    print("✅ Task added!")


def list_tasks(status=None):
    tasks = load_tasks()

    if status and status not in VALID_STATUS:
        print(f"❌ Invalid status. Use: {VALID_STATUS}")
        return

    filtered = [
        {
            "ID": t["id"],
            "Description": t["description"],
            "Status": t["status"],
            "Created": t["createdAt"],
            "Updated": t["updatedAt"]
        }
        for t in tasks
        if status is None or t["status"] == status
    ]

    if not filtered:
        print("📭 No tasks found")
        return

    print(tabulate(filtered, headers="keys", tablefmt="rounded_grid"))


def update_task(task_id, new_desc):
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == int(task_id):
            task["description"] = new_desc
            task["updatedAt"] = now()
            save_tasks(tasks)
            print("✏️ Task updated")
            return

    print("❌ Task not found")


def delete_task(task_id):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t["id"] != int(task_id)]

    if len(tasks) == len(new_tasks):
        print("❌ Task not found")
        return

    save_tasks(new_tasks)
    print("🗑️ Task deleted")


def mark_status(task_id, status):
    if status not in VALID_STATUS:
        print(f"❌ Invalid status. Use: {VALID_STATUS}")
        return

    tasks = load_tasks()

    for task in tasks:
        if task["id"] == int(task_id):
            task["status"] = status
            task["updatedAt"] = now()
            save_tasks(tasks)
            print(f"🔄 Marked as {status}")
            return

    print("❌ Task not found")


# ---------- Command Mapping ----------
supported_queries = {
    "add": {
        "help": "Add a new task",
        "target": lambda description: add_task(description),
        "args": [
            {"name_or_flags": ["description"], "help": "Task description"}
        ],
    },
    "list": {
        "help": "List tasks",
        "target": lambda status=None: list_tasks(status),
        "args": [
            {"name_or_flags": ["status"], "nargs": "?", "default": None, "help": "Filter by status"}
        ],
    },
    "update": {
        "help": "Update a task",
        "target": lambda task_id, description: update_task(task_id, description),
        "args": [
            {"name_or_flags": ["task_id"], "help": "Task ID"},
            {"name_or_flags": ["description"], "help": "New description"},
        ],
    },
    "delete": {
        "help": "Delete a task",
        "target": lambda task_id: delete_task(task_id),
        "args": [
            {"name_or_flags": ["task_id"], "help": "Task ID"}
        ],
    },
    "progress": {
        "help": "Mark task as in progress",
        "target": lambda task_id: mark_status(task_id, "progress"),
        "args": [
            {"name_or_flags": ["task_id"], "help": "Task ID"}
        ],
    },
    "done": {
        "help": "Mark task as done",
        "target": lambda task_id: mark_status(task_id, "done"),
        "args": [
            {"name_or_flags": ["task_id"], "help": "Task ID"}
        ],
    },
}


# ---------- parse_args ----------
def parse_args() -> tuple[Callable, dict, Path]:
    parser = ArgumentParser(description="Task CLI with argparse")
    parser.add_argument("--db", default="~/taskly.json",
                        help="Path to database file")

    subparsers = parser.add_subparsers(dest="command", required=True)

    for name, props in supported_queries.items():
        p = subparsers.add_parser(name, help=props["help"])
        for arg in props["args"]:
            name_or_flags = arg["name_or_flags"]
            kwargs = {k: v for k, v in arg.items() if k != "name_or_flags"}
            p.add_argument(*name_or_flags, **kwargs)

    args = vars(parser.parse_args())
    command = args.pop("command")

    query = supported_queries[command]["target"]
    db_path = Path(args.pop("db")).expanduser().resolve()

    if db_path.is_dir():
        parser.error(f"Database path '{db_path}' is a directory")

    return query, args, db_path


# ---------- Main ----------
def main():
    try:
        query, args, db_path = parse_args()

        global FILE
        FILE = str(db_path)

        query(**args)

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
import sys
import json
import os
from datetime import datetime
from tabulate import tabulate

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


# ---------- CLI ----------
def show_help():
    print("""
📌 Task CLI Usage:

python task_cli.py add "task description"
python task_cli.py list
python task_cli.py list done
python task_cli.py update <id> "new description"
python task_cli.py delete <id>
python task_cli.py progress <id>
python task_cli.py done <id>
""")


def main():
    args = sys.argv

    if len(args) < 2:
        show_help()
        return

    command = args[1]

    try:
        if command == "add":
            add_task(" ".join(args[2:]))

        elif command == "list":
            list_tasks(args[2] if len(args) > 2 else None)

        elif command == "update":
            update_task(args[2], " ".join(args[3:]))

        elif command == "delete":
            delete_task(args[2])

        elif command == "progress":
            mark_status(args[2], "progress")

        elif command == "done":
            mark_status(args[2], "done")

        elif command == "help":
            show_help()

        else:
            print("❌ Unknown command")
            show_help()

    except IndexError:
        print("❌ Missing arguments. Use 'help' command.")


if __name__ == "__main__":
    main()
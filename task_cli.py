import sys
import json
import os
from datetime import datetime
from tabulate import tabulate

FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(FILE):
        return []
    
    with open(FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(FILE, "w") as f:
        json.dump(tasks, f, indent=4)


def add_task(description):
    tasks = load_tasks()

    task = {
        "id": len(tasks) + 1,
        "description": description,
        "status": "todo",
        "createdAt": str(datetime.now()),
        "updatedAt": str(datetime.now())
    }

    tasks.append(task)
    save_tasks(tasks)

    print("Task added successfully!")


def list_tasks(status=None):
    tasks = load_tasks()
    table = []
    for task in tasks:
        if status is None or task["status"] == status:
            # print(f'{task["id"]} | {task["description"]} | {task["status"]} | {task["createdAt"]} | {task["updatedAt"]}')
            table.append({
                "Id": task["id"],
                "Description": task["description"],
                "Status": task["status"],
                "Created At": task["createdAt"],
                "Updated At": task["updatedAt"]
            })
            
    print(tabulate(table, tablefmt="rounded_grid", headers="keys") or "Nothing to display")


def update_task(task_id, new_desc):
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == int(task_id):
            task["description"] = new_desc
            task["updatedAt"] = str(datetime.now())
            save_tasks(tasks)
            print("Task updated")
            return

    print("Task not found")

def delete_task(task_id):
    tasks = load_tasks()

    tasks = [t for t in tasks if t["id"] != int(task_id)]

    save_tasks(tasks)
    print("Task deleted")

def mark_status(task_id, status):
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == int(task_id):
            task["status"] = status
            save_tasks(tasks)
            print("Status updated")
            return

    print("Task not found")

def main():
    args = sys.argv

    if len(args) < 2:
        print("Usage: python task_cli.py [command]")
        return

    command = args[1]

    if command == "add":
        add_task(args[2])

    elif command == "list":
        if len(args) == 3:
            list_tasks(args[2])
        else:
            list_tasks()

    elif command == "update":
        update_task(args[2], args[3])

    elif command == "delete":
        delete_task(args[2])

    elif command == "progress":
        mark_status(args[2], "progress")

    elif command == "done":
        mark_status(args[2], "done")

    else:
        print("Unknown command")

if __name__ == "__main__":
    main()


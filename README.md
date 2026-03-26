# 📝 Taskly CLI – Task Manager in Python

A simple and powerful **command-line task manager** built with Python.  
It allows you to manage your daily tasks efficiently using a JSON file as storage.

---

## 🚀 Features

- ➕ Add new tasks  
- 📋 List all tasks (with optional filtering)  
- ✏️ Update task descriptions  
- 🗑️ Delete tasks  
- 🔄 Mark tasks as:
  - `todo`
  - `progress`
  - `done`  
- 💾 Persistent storage using JSON  
- 📊 Clean table output using `tabulate`  
- 📁 Custom database file path support  

---

## 🛠️ Installation

### 1. Clone the repository

    git clone https://github.com/your-username/taskly-cli.git
    cd taskly-cli

### 2. Install dependencies

    pip install tabulate

---

## ⚙️ Usage

Run the script using:

    python main.py <command> [arguments]

---

## 📌 Commands

### ➕ Add a Task

    python main.py add "Buy groceries"

---

### 📋 List Tasks

    python main.py list

Filter by status:

    python main.py list todo
    python main.py list progress
    python main.py list done

---

### ✏️ Update a Task

    python main.py update 1 "Buy groceries and fruits"

---

### 🗑️ Delete a Task

    python main.py delete 1

---

### 🔄 Mark Task Status

Mark as **in progress**:

    python main.py progress 1

Mark as **done**:

    python main.py done 1

---

## 📁 Custom Database Path

You can specify a custom JSON file for storing tasks:

    python main.py --db ~/mytasks.json add "New Task"

---

## 📊 Example Output

    ╭────┬───────────────────────┬───────────┬───────────────────────┬───────────────────────╮
    │ ID │ Description           │ Status    │ Created               │ Updated               │
    ├────┼───────────────────────┼───────────┼───────────────────────┼───────────────────────┤
    │ 1  │ Buy groceries         │ todo      │ 2026-03-26 10:00:00   │ 2026-03-26 10:00:00   │
    ╰────┴───────────────────────┴───────────┴───────────────────────┴───────────────────────╯

---

## 🧠 Project Structure

    .
    ├── main.py        # Main CLI application
    ├── tasks.json     # Default task storage (auto-created)
    └── README.md      # Documentation

---

## ⚠️ Notes

- If the JSON file is corrupted or empty, it will reset automatically.
- Task IDs are auto-incremented.
- Invalid commands or statuses will show error messages.

---
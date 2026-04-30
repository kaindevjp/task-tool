import json
import os

TASKS_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")


def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def add_task(title):
    tasks = load_tasks()
    new_id = max((t["id"] for t in tasks), default=0) + 1
    from datetime import datetime
    task = {
        "id": new_id,
        "title": title,
        "done": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"タスクを追加しました: [{new_id}] {title}")

import json
import os

# tasks.json のパスをスクリプトと同じディレクトリに固定する
TASKS_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")


def load_tasks():
    # ファイルが存在しない場合（初回起動時）は空リストを返す
    if not os.path.exists(TASKS_FILE):
        return []
    # json.load() でJSONをPythonのリストに変換して返す
    with open(TASKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tasks(tasks):
    # ensure_ascii=False で日本語をそのまま保存、indent=2 で読みやすく整形
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def add_task(title):
    tasks = load_tasks()
    # 既存IDの最大値に+1してユニークなIDを採番（タスクが0件のときは default=0 で1始まりにする）
    new_id = max((t["id"] for t in tasks), default=0) + 1
    from datetime import datetime
    task = {
        "id": new_id,
        "title": title,
        "done": False,  # 追加時は必ず未完了
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"タスクを追加しました: [{new_id}] {title}")


def list_tasks():
    tasks = load_tasks()
    # タスクが1件もない場合はメッセージを表示して終了
    if not tasks:
        print("タスクはありません")
        return
    for task in tasks:
        # done は bool なので、表示用の文字列に変換する
        status = "完了" if task["done"] else "未完了"
        print(f"[{task['id']}] {status} | {task['title']} | 作成: {task['created_at']}")


def done_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks(tasks)
            print(f"タスクを完了にしました: [{task_id}] {task['title']}")
            return  # 見つかったら即return（残りのループは不要）
    # ループを最後まで回っても見つからなかった場合
    print(f"ID {task_id} のタスクが見つかりません")


def delete_task(task_id):
    tasks = load_tasks()
    # 対象ID以外のタスクだけを残した新しいリストを作る
    new_tasks = [t for t in tasks if t["id"] != task_id]
    # 件数が変わっていなければ対象IDが存在しなかった
    if len(new_tasks) == len(tasks):
        print(f"ID {task_id} のタスクが見つかりません")
        return
    save_tasks(new_tasks)
    print(f"タスクを削除しました: ID {task_id}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="タスク管理CLIツール")
    # サブコマンド（add/list/done/delete）を登録する。dest="command" で args.command に格納される
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="タスクを追加する")
    add_parser.add_argument("title", help="タスクのタイトル")

    subparsers.add_parser("list", help="タスク一覧を表示する")

    done_parser = subparsers.add_parser("done", help="タスクを完了にする")
    done_parser.add_argument("id", type=int, help="完了にするタスクのID")  # type=int で自動キャスト

    delete_parser = subparsers.add_parser("delete", help="タスクを削除する")
    delete_parser.add_argument("id", type=int, help="削除するタスクのID")

    args = parser.parse_args()

    # args.command の値でどの関数を呼ぶか振り分ける
    if args.command == "add":
        add_task(args.title)
    elif args.command == "list":
        list_tasks()
    elif args.command == "done":
        done_task(args.id)
    elif args.command == "delete":
        delete_task(args.id)
    else:
        # サブコマンドなしで実行された場合はヘルプを表示
        parser.print_help()


# python task.py で直接実行されたときだけ main() を呼ぶ
if __name__ == "__main__":
    main()

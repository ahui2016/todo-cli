import json
import arrow
from pathlib import Path
from typing import cast
from appdirs import AppDirs

from simpletodo.model import DB, Repeat, TodoList, TodoStatus, new_db

todo_db_name = "todo-db.json"

app_dirs = AppDirs("todo", "github-ahui2016")
app_config_dir = Path(app_dirs.user_config_dir)
db_path = app_config_dir.joinpath(todo_db_name)


def ensure_db_file() -> None:
    app_config_dir.mkdir(parents=True, exist_ok=True)
    if not db_path.exists():
        with open(db_path, "w", encoding="utf-8") as f:
            json.dump(new_db(), f, indent=4, ensure_ascii=False)


def load_db() -> DB:
    with open(db_path, "rb") as f:
        return cast(DB, json.load(f))


def split_db(db: DB) -> tuple[TodoList, TodoList, TodoList]:
    todo_list: TodoList = []
    done_list: TodoList = []
    repeat_list: TodoList = []
    for item in db["items"]:
        if TodoStatus[item["status"]] is TodoStatus.Incomplete:
            todo_list.append(item)
        if item["dtime"] > 0:
            done_list.append(item)
        if Repeat[item["repeat"]] is not Repeat.Never:
            repeat_list.append(item)
    todo_list.sort(key=lambda x: x["ctime"], reverse=True)
    done_list.sort(key=lambda x: x["dtime"], reverse=True)
    repeat_list.sort(key=lambda x: x["ntime"], reverse=True)
    return todo_list, done_list, repeat_list


def update_db(db: DB) -> None:
    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=4, ensure_ascii=False)


def print_todolist(l: TodoList) -> None:
    if not l:
        return
    print("\nTodo\n------------")
    for idx, item in enumerate(l):
        print(f"{idx+1}. {item['event']}")


def print_donelist(l: TodoList) -> None:
    if not l:
        return
    print("\nCompleted\n------------")
    for idx, item in enumerate(l):
        print(f"{idx+1}. {item['event']}")


def print_repeatlist(l: TodoList) -> None:
    print("\nSchedule\n------------")
    for idx, item in enumerate(l):
        reminder = arrow.get(item["ntime"]).format("YYYY-MM-DD")
        print(f"{idx+1}. [{reminder}] {item['event']}")
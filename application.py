import json
import os
from datetime import datetime

APPLICATIONS_FILE = "applications.json"


def _load_json(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default


def _save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_applications(path=APPLICATIONS_FILE):
    data = _load_json(path, [])
    return data if isinstance(data, list) else []


def save_applications(applications, path=APPLICATIONS_FILE):
    _save_json(path, applications)


def next_application_id(applications):
    return max((a.get("id", 0) for a in applications), default=0) + 1


def find_application(applications, application_id):
    for a in applications:
        if a["id"] == application_id:
            return a
    return None


def has_active_application(applications, project_id, user_id):
    for a in applications:
        if (a["project_id"] == project_id
                and a["user_id"] == user_id
                and a["status"] == "active"):
            return True
    return False


def add_application(applications, project, user):
    if project is None:
        return None, "Проект не найден."
    if user is None:
        return None, "Пользователь не найден."
    if not project["current_participants"] < project["max_participants"]:
        return None, "Нет свободных мест — проект недоступен."
    if has_active_application(applications, project["id"], user["id"]):
        return None, "Пользователь уже подал заявку на этот проект."

    application = {
        "id": next_application_id(applications),
        "project_id": project["id"],
        "user_id": user["id"],
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": "active",
    }
    applications.append(application)
    project["current_participants"] += 1
    return application, "Заявка добавлена."


def cancel_application(applications, project, application_id):
    application = find_application(applications, application_id)
    if application is None:
        return False, "Заявка не найдена."
    if application["status"] != "active":
        return False, "Заявка уже отменена."
    application["status"] = "cancelled"
    if project and project["current_participants"] > 0:
        project["current_participants"] -= 1
    return True, "Заявка отменена."
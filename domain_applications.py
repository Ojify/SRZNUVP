"""Сущность «Заявка»."""

from datetime import datetime

from storage import load_json, save_json
from utils import next_id

FILE = "applications.json"


def load_applications():
    data = load_json(FILE, [])
    return data if isinstance(data, list) else []


def save_applications(applications):
    save_json(FILE, applications)


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
    if project["current_participants"] >= project["max_participants"]:
        return None, "Нет свободных мест — проект недоступен."
    if has_active_application(applications, project["id"], user["id"]):
        return None, "Пользователь уже подал заявку на этот проект."

    application = {
        "id": next_id(applications),
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


def get_statistics(projects, applications):
    total_places = sum(p["max_participants"] for p in projects.values())
    taken = sum(p["current_participants"] for p in projects.values())
    active = [a for a in applications if a["status"] == "active"]
    fill = round(taken / total_places * 100, 2) if total_places else 0.0
    return {
        "total_projects": len(projects),
        "active_applications": len(active),
        "cancelled_applications": len(applications) - len(active),
        "total_places": total_places,
        "taken_places": taken,
        "free_places": max(0, total_places - taken),
        "fill_percent": fill,
    }
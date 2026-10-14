"""Сущность «Проект»."""

from storage import load_json, save_json
from utils import next_id

FILE = "projects.json"


def load_projects():
    raw = load_json(FILE, {})
    projects = {}
    if not isinstance(raw, dict):
        return projects
    for key, value in raw.items():
        try:
            pid = int(key)
        except (TypeError, ValueError):
            continue
        value["id"] = pid
        value["max_participants"] = int(value.get("max_participants", 0))
        value["current_participants"] = int(value.get("current_participants", 0))
        projects[pid] = value
    return projects


def save_projects(projects):
    save_json(FILE, {str(k): v for k, v in projects.items()})


def find_project(projects, project_id):
    return projects.get(project_id)


def check_availability(project):
    return project["current_participants"] < project["max_participants"]


def free_places(project):
    return max(0, project["max_participants"] - project["current_participants"])


def add_project(projects, name, description, deadline, max_participants):
    pid = next_id(projects)
    projects[pid] = {
        "id": pid,
        "name": name,
        "description": description,
        "deadline": deadline,
        "max_participants": int(max_participants),
        "current_participants": 0,
    }
    return pid


def edit_project(projects, project_id, name=None, description=None,
                 deadline=None, max_participants=None):
    project = projects.get(project_id)
    if project is None:
        return False
    if name:
        project["name"] = name
    if description:
        project["description"] = description
    if deadline:
        project["deadline"] = deadline
    if max_participants is not None and max_participants > 0:
        if max_participants >= project["current_participants"]:
            project["max_participants"] = int(max_participants)
    return True


def delete_project(projects, project_id):
    if project_id not in projects:
        return False
    del projects[project_id]
    return True


def search_projects(projects, query):
    q = (query or "").strip().lower()
    values = list(projects.values())
    if not q:
        return values
    return [p for p in values
            if q in p["name"].lower() or q in p["description"].lower()]


def sort_projects(projects, key="name", reverse=False):
    values = list(projects.values())
    keys = {
        "id": lambda p: p["id"],
        "name": lambda p: p["name"].lower(),
        "deadline": lambda p: p["deadline"],
        "participants": lambda p: p["current_participants"],
    }
    values.sort(key=keys.get(key, keys["name"]), reverse=reverse)
    return values
import json
import os

PROJECTS_FILE = "projects.json"


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


def load_projects(path=PROJECTS_FILE):
    raw = _load_json(path, {})
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


def save_projects(projects, path=PROJECTS_FILE):
    _save_json(path, {str(k): v for k, v in projects.items()})


def next_project_id(projects):
    return max(projects.keys(), default=0) + 1


def find_project(projects, project_id):
    return projects.get(project_id)


def check_availability(project):
    return project["current_participants"] < project["max_participants"]


def free_places(project):
    return max(0, project["max_participants"] - project["current_participants"])


def add_project(projects, name, description, deadline, max_participants):
    pid = next_project_id(projects)
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
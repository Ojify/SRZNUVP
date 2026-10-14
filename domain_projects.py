"""Сущность «Проект»."""

from typing import Dict, List, Optional

from storage import load_json, save_json
from utils import next_id

FILE = "projects.json"


class Project:
    """Проект — инициатива, в которую подаются заявки."""

    def __init__(
        self,
        project_id: int,
        name: str,
        description: str,
        deadline: str,
        max_participants: int,
        current_participants: int = 0,
    ) -> None:
        self.id = project_id
        self.name = name
        self.description = description
        self.deadline = deadline
        self.max_participants = int(max_participants)
        self.current_participants = int(current_participants)

    def is_available(self) -> bool:
        return self.current_participants < self.max_participants

    def free_places(self) -> int:
        return max(
            0, self.max_participants - self.current_participants
        )

    def __str__(self) -> str:
        return (
            f"[{self.id}] {self.name}  "
            f"({self.current_participants}/{self.max_participants}, "
            f"свободно: {self.free_places()})"
        )

    @classmethod
    def from_data(cls, data: dict) -> "Project":
        return cls(
            project_id=int(data["id"]),
            name=data["name"],
            description=data["description"],
            deadline=data["deadline"],
            max_participants=int(data.get("max_participants", 0)),
            current_participants=int(
                data.get("current_participants", 0)
            ),
        )

    def to_data(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "deadline": self.deadline,
            "max_participants": self.max_participants,
            "current_participants": self.current_participants,
        }


def load_projects(path: str = FILE) -> Dict[int, Project]:
    raw = load_json(path, {})
    projects: Dict[int, Project] = {}
    if not isinstance(raw, dict):
        return projects
    for key, value in raw.items():
        try:
            value = dict(value)
            value["id"] = int(key)
            projects[value["id"]] = Project.from_data(value)
        except (TypeError, ValueError, KeyError):
            continue
    return projects


def save_projects(
    projects: Dict[int, Project], path: str = FILE
) -> None:
    save_json(
        path,
        {str(pid): p.to_data() for pid, p in projects.items()},
    )


def find_project(
    projects: Dict[int, Project], project_id: int
) -> Optional[Project]:
    return projects.get(project_id)


def check_availability(project: Optional[Project]) -> bool:
    if project is None:
        return False
    return project.is_available()


def free_places(project: Optional[Project]) -> int:
    if project is None:
        return 0
    return project.free_places()


def add_project(
    projects: Dict[int, Project],
    name: str,
    description: str,
    deadline: str,
    max_participants: int,
) -> int:
    pid = next_id(projects)
    projects[pid] = Project(
        project_id=pid,
        name=name,
        description=description,
        deadline=deadline,
        max_participants=max_participants,
        current_participants=0,
    )
    return pid


def edit_project(
    projects: Dict[int, Project],
    project_id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
    deadline: Optional[str] = None,
    max_participants: Optional[int] = None,
) -> bool:
    project = projects.get(project_id)
    if project is None:
        return False
    if name:
        project.name = name
    if description:
        project.description = description
    if deadline:
        project.deadline = deadline
    if max_participants is not None and max_participants > 0:
        if max_participants >= project.current_participants:
            project.max_participants = int(max_participants)
    return True


def delete_project(
    projects: Dict[int, Project], project_id: int
) -> bool:
    if project_id not in projects:
        return False
    del projects[project_id]
    return True


def search_projects(
    projects: Dict[int, Project], query: str
) -> List[Project]:
    q = (query or "").strip().lower()
    if not q:
        return list(projects.values())
    return [
        p for p in projects.values()
        if q in p.name.lower() or q in p.description.lower()
    ]


def sort_projects(
    projects: Dict[int, Project],
    key: str = "name",
    reverse: bool = False,
) -> List[Project]:
    values = list(projects.values())
    keys = {
        "id": lambda p: p.id,
        "name": lambda p: p.name.lower(),
        "deadline": lambda p: p.deadline,
        "participants": lambda p: p.current_participants,
    }
    values.sort(key=keys.get(key, keys["name"]), reverse=reverse)
    return values

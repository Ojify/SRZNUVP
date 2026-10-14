"""Сущность «Заявка»."""

from datetime import datetime
from typing import Dict, List, Optional, Tuple

from domain_projects import Project
from domain_users import User
from storage import load_json, save_json
from utils import next_id

FILE = "applications.json"


class Application:
    """Заявка на участие в проекте."""

    def __init__(
        self,
        application_id: int,
        project: Project,
        user: User,
        created_at: str,
        status: str = "active",
    ) -> None:
        self.id = application_id
        self.project = project
        self.user = user
        self.created_at = created_at
        self.status = status

    def is_active(self) -> bool:
        return self.status == "active"

    def cancel(self) -> None:
        self.status = "cancelled"

    def __str__(self) -> str:
        return (
            f"[{self.id}] {self.user.name} → «{self.project.name}»  "
            f"статус: {self.status}  ({self.created_at})"
        )

    def to_data(self) -> dict:
        return {
            "id": self.id,
            "project_id": self.project.id,
            "user_id": self.user.id,
            "created_at": self.created_at,
            "status": self.status,
        }


def load_applications(
    projects: Dict[int, Project],
    users: Dict[int, User],
    path: str = FILE,
) -> List[Application]:
    raw = load_json(path, [])
    applications: List[Application] = []
    if not isinstance(raw, list):
        return applications
    for item in raw:
        try:
            project = projects.get(int(item["project_id"]))
            user = users.get(int(item["user_id"]))
            if project is None or user is None:
                continue
            applications.append(Application(
                application_id=int(item["id"]),
                project=project,
                user=user,
                created_at=item["created_at"],
                status=item.get("status", "active"),
            ))
        except (TypeError, ValueError, KeyError):
            continue
    return applications


def save_applications(
    applications: List[Application], path: str = FILE
) -> None:
    save_json(path, [a.to_data() for a in applications])


def find_application(
    applications: List[Application], application_id: int
) -> Optional[Application]:
    for a in applications:
        if a.id == application_id:
            return a
    return None


def has_active_application(
    applications: List[Application],
    project_id: int,
    user_id: int,
) -> bool:
    for a in applications:
        if (
            a.project.id == project_id
            and a.user.id == user_id
            and a.is_active()
        ):
            return True
    return False


def add_application(
    applications: List[Application],
    project: Optional[Project],
    user: Optional[User],
) -> Tuple[Optional[Application], str]:
    if project is None:
        return None, "Проект не найден."
    if user is None:
        return None, "Пользователь не найден."
    if not project.is_available():
        return None, "Нет свободных мест — проект недоступен."
    if has_active_application(
        applications, project.id, user.id
    ):
        return None, "Пользователь уже подал заявку на этот проект."

    application = Application(
        application_id=next_id(applications),
        project=project,
        user=user,
        created_at=datetime.now().isoformat(timespec="seconds"),
        status="active",
    )
    applications.append(application)
    project.current_participants += 1
    return application, "Заявка добавлена."


def cancel_application(
    applications: List[Application],
    project: Optional[Project],
    application_id: int,
) -> Tuple[bool, str]:
    application = find_application(applications, application_id)
    if application is None:
        return False, "Заявка не найдена."
    if not application.is_active():
        return False, "Заявка уже отменена."
    application.cancel()
    if project and project.current_participants > 0:
        project.current_participants -= 1
    return True, "Заявка отменена."


def get_statistics(
    projects: Dict[int, Project],
    applications: List[Application],
) -> dict:
    total_places = sum(
        p.max_participants for p in projects.values()
    )
    taken = sum(
        p.current_participants for p in projects.values()
    )
    active = [a for a in applications if a.is_active()]
    fill = (
        round(taken / total_places * 100, 2)
        if total_places else 0.0
    )
    return {
        "total_projects": len(projects),
        "active_applications": len(active),
        "cancelled_applications": len(applications) - len(active),
        "total_places": total_places,
        "taken_places": taken,
        "free_places": max(0, total_places - taken),
        "fill_percent": fill,
    }

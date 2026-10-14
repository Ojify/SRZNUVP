"""Сущность «Пользователь»."""

from typing import Dict, List, Optional

from storage import load_json, save_json
from utils import next_id

FILE = "users.json"


class User:
    """Пользователь системы."""

    def __init__(
        self,
        user_id: int,
        name: str,
        email: str,
        skills: Optional[List[str]] = None,
    ) -> None:
        self.id = user_id
        self.name = name
        self.email = email
        self.skills: List[str] = list(skills or [])

    def __str__(self) -> str:
        skills = ", ".join(self.skills) or "—"
        return f"[{self.id}] {self.name} <{self.email}>  навыки: {skills}"

    @classmethod
    def from_data(cls, data: dict) -> "User":
        return cls(
            user_id=int(data["id"]),
            name=data["name"],
            email=data["email"],
            skills=list(data.get("skills", [])),
        )

    def to_data(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "skills": list(self.skills),
        }


def load_users(path: str = FILE) -> Dict[int, User]:
    raw = load_json(path, {})
    users: Dict[int, User] = {}
    if not isinstance(raw, dict):
        return users
    for key, value in raw.items():
        try:
            value = dict(value)
            value["id"] = int(key)
            users[value["id"]] = User.from_data(value)
        except (TypeError, ValueError, KeyError):
            continue
    return users


def save_users(users: Dict[int, User], path: str = FILE) -> None:
    save_json(path, {str(uid): u.to_data() for uid, u in users.items()})


def find_user(
    users: Dict[int, User], user_id: int
) -> Optional[User]:
    return users.get(user_id)


def add_user(
    users: Dict[int, User],
    name: str,
    email: str,
    skills: Optional[List[str]] = None,
) -> int:
    uid = next_id(users)
    users[uid] = User(uid, name, email, skills)
    return uid


def edit_user(
    users: Dict[int, User],
    user_id: int,
    name: Optional[str] = None,
    email: Optional[str] = None,
    skills: Optional[List[str]] = None,
) -> bool:
    user = users.get(user_id)
    if user is None:
        return False
    if name:
        user.name = name
    if email:
        user.email = email
    if skills is not None:
        user.skills = list(skills)
    return True


def delete_user(users: Dict[int, User], user_id: int) -> bool:
    if user_id not in users:
        return False
    del users[user_id]
    return True


def search_users(
    users: Dict[int, User], query: str
) -> List[User]:
    q = (query or "").strip().lower()
    if not q:
        return list(users.values())
    return [
        u for u in users.values()
        if q in u.name.lower() or q in u.email.lower()
    ]

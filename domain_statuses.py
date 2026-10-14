"""Сущность «Статус»."""

from typing import Dict, List, Optional

from storage import load_json, save_json

FILE = "statuses.json"


class Status:
    """Статус заявки."""

    def __init__(
        self, code: str, name: str, description: str
    ) -> None:
        self.code = code
        self.name = name
        self.description = description

    def __str__(self) -> str:
        return f"[{self.code}] {self.name} — {self.description}"

    @classmethod
    def from_data(cls, data: dict) -> "Status":
        return cls(
            code=data["code"],
            name=data["name"],
            description=data["description"],
        )

    def to_data(self) -> dict:
        return {
            "code": self.code,
            "name": self.name,
            "description": self.description,
        }


DEFAULT_STATUSES = {
    "active": Status(
        "active", "Активна", "Заявка подана и рассматривается"
    ),
    "cancelled": Status(
        "cancelled", "Отменена", "Заявка отменена пользователем"
    ),
    "approved": Status(
        "approved", "Одобрена", "Заявка принята организатором"
    ),
    "rejected": Status(
        "rejected", "Отклонена", "Заявка отклонена организатором"
    ),
}


def load_statuses(path: str = FILE) -> Dict[str, Status]:
    data = load_json(path, None)
    if not isinstance(data, dict) or not data:
        return {
            code: Status.from_data(s.to_data())
            for code, s in DEFAULT_STATUSES.items()
        }
    statuses: Dict[str, Status] = {}
    for code, value in data.items():
        try:
            statuses[code] = Status.from_data(value)
        except (TypeError, KeyError):
            continue
    return statuses


def save_statuses(
    statuses: Dict[str, Status], path: str = FILE
) -> None:
    save_json(
        path,
        {code: s.to_data() for code, s in statuses.items()},
    )


def get_status(
    statuses: Dict[str, Status], code: str
) -> Optional[Status]:
    return statuses.get(code)


def list_statuses(statuses: Dict[str, Status]) -> List[Status]:
    return list(statuses.values())


def is_valid_status(statuses: Dict[str, Status], code: str) -> bool:
    return code in statuses

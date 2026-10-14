"""Сущность «Статус»."""

from storage import load_json, save_json

FILE = "statuses.json"

DEFAULT_STATUSES = {
    "active": {
        "code": "active",
        "name": "Активна",
        "description": "Заявка подана и рассматривается",
    },
    "cancelled": {
        "code": "cancelled",
        "name": "Отменена",
        "description": "Заявка отменена пользователем",
    },
    "approved": {
        "code": "approved",
        "name": "Одобрена",
        "description": "Заявка принята организатором",
    },
    "rejected": {
        "code": "rejected",
        "name": "Отклонена",
        "description": "Заявка отклонена организатором",
    },
}


def load_statuses():
    data = load_json(FILE, None)
    if not isinstance(data, dict) or not data:
        return {code: dict(v) for code, v in DEFAULT_STATUSES.items()}
    return data


def save_statuses(statuses):
    save_json(FILE, statuses)


def get_status(statuses, code):
    return statuses.get(code)


def list_statuses(statuses):
    return list(statuses.values())


def is_valid_status(statuses, code):
    return code in statuses
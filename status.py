import json
import os

STATUSES_FILE = "statuses.json"

DEFAULT_STATUSES = {
    "active":    {"code": "active",    "name": "Активна",   "description": "Заявка подана и рассматривается"},
    "cancelled": {"code": "cancelled", "name": "Отменена",  "description": "Заявка отменена пользователем"},
    "approved":  {"code": "approved",  "name": "Одобрена",  "description": "Заявка принята организатором"},
    "rejected":  {"code": "rejected",  "name": "Отклонена", "description": "Заявка отклонена организатором"},
}


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


def load_statuses(path=STATUSES_FILE):
    data = _load_json(path, None)
    if not isinstance(data, dict) or not data:
        return {code: dict(v) for code, v in DEFAULT_STATUSES.items()}
    return data


def save_statuses(statuses, path=STATUSES_FILE):
    _save_json(path, statuses)


def get_status(statuses, code):
    return statuses.get(code)


def list_statuses(statuses):
    return list(statuses.values())


def is_valid_status(statuses, code):
    return code in statuses
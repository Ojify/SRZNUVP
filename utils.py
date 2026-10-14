"""Общие вспомогательные функции."""

from datetime import datetime

DATE_FORMAT = "%Y-%m-%d"


def parse_date(raw):
    return datetime.strptime(raw.strip(), DATE_FORMAT).date().isoformat()


def parse_int(raw):
    return int(str(raw).strip())


def parse_positive_int(raw):
    value = parse_int(raw)
    if value <= 0:
        raise ValueError("Значение должно быть больше нуля.")
    return value


def parse_skills(raw):
    if not raw:
        return []
    return [s.strip() for s in raw.split(",") if s.strip()]


def next_id(collection):
    if isinstance(collection, dict):
        keys = collection.keys()
    else:
        keys = [item.get("id", 0) for item in collection]
    return max(keys, default=0) + 1

"""Общий слой чтения/записи JSON."""

import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def data_path(filename):
    ensure_data_dir()
    return os.path.join(DATA_DIR, filename)


def load_json(filename, default):
    path = data_path(filename)
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default


def save_json(filename, data):
    path = data_path(filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

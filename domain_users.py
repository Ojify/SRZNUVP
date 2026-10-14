"""Сущность «Пользователь»."""

from storage import load_json, save_json
from utils import next_id

FILE = "users.json"


def load_users():
    raw = load_json(FILE, {})
    users = {}
    if not isinstance(raw, dict):
        return users
    for key, value in raw.items():
        try:
            uid = int(key)
        except (TypeError, ValueError):
            continue
        value["id"] = uid
        value.setdefault("skills", [])
        users[uid] = value
    return users


def save_users(users):
    save_json(FILE, {str(k): v for k, v in users.items()})


def find_user(users, user_id):
    return users.get(user_id)


def add_user(users, name, email, skills=None):
    uid = next_id(users)
    users[uid] = {
        "id": uid,
        "name": name,
        "email": email,
        "skills": list(skills or []),
    }
    return uid


def edit_user(users, user_id, name=None, email=None, skills=None):
    user = users.get(user_id)
    if user is None:
        return False
    if name:
        user["name"] = name
    if email:
        user["email"] = email
    if skills is not None:
        user["skills"] = list(skills)
    return True


def delete_user(users, user_id):
    if user_id not in users:
        return False
    del users[user_id]
    return True


def search_users(users, query):
    q = (query or "").strip().lower()
    values = list(users.values())
    if not q:
        return values
    return [u for u in values
            if q in u["name"].lower() or q in u["email"].lower()]
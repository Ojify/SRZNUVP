import json
import os

USERS_FILE = "users.json"


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


def load_users(path=USERS_FILE):
    raw = _load_json(path, {})
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


def save_users(users, path=USERS_FILE):
    _save_json(path, {str(k): v for k, v in users.items()})


def next_user_id(users):
    return max(users.keys(), default=0) + 1


def find_user(users, user_id):
    return users.get(user_id)


def add_user(users, name, email, skills=None):
    uid = next_user_id(users)
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
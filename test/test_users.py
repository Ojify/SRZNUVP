import domain_users as user_mod
from domain_users import User


def test_user_creation():
    u = User(1, "Иван", "i@e.com", ["python", "sql"])
    assert u.id == 1
    assert u.name == "Иван"
    assert u.email == "i@e.com"
    assert u.skills == ["python", "sql"]


def test_user_str_and_from_data():
    u = User.from_data(
        {"id": 2, "name": "Аня", "email": "a@e.com", "skills": ["sql"]}
    )
    assert u.id == 2
    assert "Аня" in str(u)
    assert u.to_data()["skills"] == ["sql"]


def test_user_default_skills():
    u = User(3, "Пётр", "p@e.com")
    assert u.skills == []


def test_users_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setattr("storage.DATA_DIR", str(tmp_path))
    users = {
        1: User(1, "A", "a@e.com"),
        2: User(2, "B", "b@e.com", ["go"]),
    }
    user_mod.save_users(users)
    loaded = user_mod.load_users()
    assert set(loaded.keys()) == {1, 2}
    assert loaded[1].name == "A"
    assert loaded[2].skills == ["go"]
    assert isinstance(loaded[1], User)


def test_add_find_edit_delete_user(tmp_path, monkeypatch):
    monkeypatch.setattr("storage.DATA_DIR", str(tmp_path))
    users = {}
    uid = user_mod.add_user(users, "Иван", "i@e.com")
    assert uid in users
    assert user_mod.find_user(users, uid) is users[uid]

    assert user_mod.edit_user(users, uid, name="Пётр") is True
    assert users[uid].name == "Пётр"

    assert user_mod.edit_user(users, 999, name="X") is False

    assert user_mod.delete_user(users, uid) is True
    assert users == {}


def test_search_users(tmp_path, monkeypatch):
    monkeypatch.setattr("storage.DATA_DIR", str(tmp_path))
    users = {
        1: User(1, "Иван Петров", "ivan@example.com", ["python"]),
        2: User(2, "Анна Смирнова", "anna@example.com", ["ui"]),
    }
    assert [
        u.id for u in user_mod.search_users(users, "анна")
    ] == [2]
    assert [
        u.id for u in user_mod.search_users(users, "ivan@")
    ] == [1]
    assert len(user_mod.search_users(users, "")) == 2

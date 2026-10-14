import pytest

import domain_users as user_mod


@pytest.fixture
def sample_users():
    return {
        1: {"id": 1, "name": "Иван Петров", "email": "ivan@example.com",
            "skills": ["python", "sql"]},
        2: {"id": 2, "name": "Анна Смирнова", "email": "anna@example.com",
            "skills": ["ui", "ux"]},
    }


def test_add_user(sample_users):
    uid = user_mod.add_user(sample_users, "Пётр", "p@example.com", ["go"])
    assert uid == 3
    assert sample_users[3]["skills"] == ["go"]


def test_edit_user(sample_users):
    ok = user_mod.edit_user(sample_users, 1, email="new@example.com")
    assert ok is True
    assert sample_users[1]["email"] == "new@example.com"
    assert sample_users[1]["name"] == "Иван Петров"


def test_edit_user_not_found(sample_users):
    assert user_mod.edit_user(sample_users, 999, name="X") is False


def test_delete_user(sample_users):
    assert user_mod.delete_user(sample_users, 2) is True
    assert 2 not in sample_users


def test_find_user(sample_users):
    assert user_mod.find_user(sample_users, 1)["name"] == "Иван Петров"
    assert user_mod.find_user(sample_users, 999) is None


def test_search_users_by_name(sample_users):
    found = user_mod.search_users(sample_users, "анна")
    assert len(found) == 1
    assert found[0]["id"] == 2


def test_search_users_by_email(sample_users):
    found = user_mod.search_users(sample_users, "ivan@")
    assert len(found) == 1
    assert found[0]["id"] == 1


def test_users_roundtrip(tmp_path, monkeypatch, sample_users):
    monkeypatch.setattr("storage.DATA_DIR", str(tmp_path))
    user_mod.save_users(sample_users)
    loaded = user_mod.load_users()
    assert loaded == sample_users
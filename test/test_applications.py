import pytest

import domain_applications as app_mod


@pytest.fixture
def setup_data():
    projects = {
        1: {"id": 1, "name": "Космос", "description": "...",
            "deadline": "2030-01-01", "max_participants": 2,
            "current_participants": 0},
    }
    users = {
        1: {"id": 1, "name": "Иван", "email": "i@e.com", "skills": []},
        2: {"id": 2, "name": "Анна", "email": "a@e.com", "skills": []},
    }
    applications = []
    return projects, users, applications


def test_add_application_success(setup_data):
    projects, users, applications = setup_data
    application, msg = app_mod.add_application(
        applications, projects[1], users[1]
    )
    assert application is not None
    assert application["status"] == "active"
    assert projects[1]["current_participants"] == 1


def test_add_application_no_places(setup_data):
    projects, users, applications = setup_data
    projects[1]["current_participants"] = projects[1]["max_participants"]
    application, msg = app_mod.add_application(
        applications, projects[1], users[1]
    )
    assert application is None
    assert "мест" in msg.lower()


def test_add_application_duplicate(setup_data):
    projects, users, applications = setup_data
    app_mod.add_application(applications, projects[1], users[1])
    application, msg = app_mod.add_application(
        applications, projects[1], users[1]
    )
    assert application is None
    assert "уже" in msg.lower()


def test_add_application_project_not_found(setup_data):
    projects, users, applications = setup_data
    application, msg = app_mod.add_application(applications, None, users[1])
    assert application is None
    assert "не найден" in msg.lower()


def test_add_application_user_not_found(setup_data):
    projects, users, applications = setup_data
    application, msg = app_mod.add_application(applications, projects[1], None)
    assert application is None
    assert "не найден" in msg.lower()


def test_cancel_application(setup_data):
    projects, users, applications = setup_data
    application, _ = app_mod.add_application(applications, projects[1], users[1])
    ok, msg = app_mod.cancel_application(applications, projects[1], application["id"])
    assert ok is True
    assert application["status"] == "cancelled"
    assert projects[1]["current_participants"] == 0


def test_cancel_application_twice(setup_data):
    projects, users, applications = setup_data
    application, _ = app_mod.add_application(applications, projects[1], users[1])
    app_mod.cancel_application(applications, projects[1], application["id"])
    ok, msg = app_mod.cancel_application(applications, projects[1], application["id"])
    assert ok is False
    assert "уже" in msg.lower()


def test_cancel_application_not_found(setup_data):
    projects, users, applications = setup_data
    ok, msg = app_mod.cancel_application(applications, None, 999)
    assert ok is False
    assert "не найдена" in msg.lower()


def test_get_statistics(setup_data):
    projects, users, applications = setup_data
    app_mod.add_application(applications, projects[1], users[1])
    app_mod.add_application(applications, projects[1], users[2])
    stats = app_mod.get_statistics(projects, applications)
    assert stats["total_projects"] == 1
    assert stats["total_places"] == 2
    assert stats["taken_places"] == 2
    assert stats["active_applications"] == 2
    assert stats["free_places"] == 0


def test_get_statistics_empty():
    stats = app_mod.get_statistics({}, [])
    assert stats["total_projects"] == 0
    assert stats["fill_percent"] == 0.0


def test_applications_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setattr("storage.DATA_DIR", str(tmp_path))
    data = [{"id": 1, "project_id": 1, "user_id": 1,
             "created_at": "2025-01-01T10:00:00", "status": "active"}]
    app_mod.save_applications(data)
    assert app_mod.load_applications() == data
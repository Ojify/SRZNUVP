import domain_applications as app_mod
from domain_applications import Application
from domain_projects import Project
from domain_users import User


def _make_fixtures():
    user = User(1, "Иван", "i@e.com")
    project = Project(1, "Космос", "Марс", "2030-01-01", 2, 0)
    return user, project


def test_application_creation_and_str():
    user, project = _make_fixtures()
    a = Application(1, project, user, "2025-01-01T10:00:00")
    assert a.id == 1
    assert a.project is project
    assert a.user is user
    assert a.is_active() is True
    assert "Иван" in str(a)
    assert a.to_data()["project_id"] == 1
    assert a.to_data()["user_id"] == 1


def test_cancel_method_changes_status():
    user, project = _make_fixtures()
    a = Application(1, project, user, "2025-01-01T10:00:00")
    a.cancel()
    assert a.status == "cancelled"
    assert a.is_active() is False


def test_add_application_success():
    user, project = _make_fixtures()
    applications = []
    a, msg = app_mod.add_application(applications, project, user)
    assert a is not None
    assert a.is_active() is True
    assert a.project is project
    assert a.user is user
    assert project.current_participants == 1
    assert "добавлена" in msg.lower()


def test_add_application_no_places():
    user, project = _make_fixtures()
    project.current_participants = project.max_participants
    a, msg = app_mod.add_application([], project, user)
    assert a is None
    assert "мест" in msg.lower()


def test_add_application_duplicate():
    user, project = _make_fixtures()
    applications = []
    app_mod.add_application(applications, project, user)
    a, msg = app_mod.add_application(
        applications, project, user
    )
    assert a is None
    assert "уже" in msg.lower()


def test_add_application_unknown_user_or_project():
    user, project = _make_fixtures()
    a, msg = app_mod.add_application([], None, user)
    assert a is None and "проект" in msg.lower()
    a, msg = app_mod.add_application([], project, None)
    assert a is None and "пользовател" in msg.lower()


def test_cancel_application():
    user, project = _make_fixtures()
    applications = []
    a, _ = app_mod.add_application(applications, project, user)
    assert project.current_participants == 1
    ok, msg = app_mod.cancel_application(
        applications, project, a.id
    )
    assert ok is True
    assert a.status == "cancelled"
    assert project.current_participants == 0


def test_cancel_application_twice():
    user, project = _make_fixtures()
    applications = []
    a, _ = app_mod.add_application(applications, project, user)
    app_mod.cancel_application(applications, project, a.id)
    ok, msg = app_mod.cancel_application(
        applications, project, a.id
    )
    assert ok is False
    assert "уже" in msg.lower()


def test_cancel_application_not_found():
    ok, msg = app_mod.cancel_application([], None, 999)
    assert ok is False
    assert "не найдена" in msg.lower()


def test_applications_roundtrip_with_relations(
    tmp_path, monkeypatch
):
    monkeypatch.setattr("storage.DATA_DIR", str(tmp_path))
    user = User(1, "A", "a@e.com")
    project = Project(1, "P", "d", "2030-01-01", 3, 1)
    applications = [
        Application(
            1, project, user, "2025-01-01T10:00:00", "active"
        ),
    ]
    app_mod.save_applications(applications)

    projects = {1: project}
    users = {1: user}
    loaded = app_mod.load_applications(projects, users)
    assert len(loaded) == 1
    assert loaded[0].project is project
    assert loaded[0].user is user
    assert loaded[0].status == "active"


def test_applications_skip_broken_relations(
    tmp_path, monkeypatch
):
    monkeypatch.setattr("storage.DATA_DIR", str(tmp_path))
    user = User(1, "A", "a@e.com")
    project = Project(1, "P", "d", "2030-01-01", 3, 0)
    applications = [
        Application(1, project, user, "2025-01-01T10:00:00"),
    ]
    app_mod.save_applications(applications)

    loaded = app_mod.load_applications({}, {1: user})
    assert loaded == []


def test_get_statistics():
    user = User(1, "A", "a@e.com")
    projects = {
        1: Project(1, "P1", "d", "2030-01-01", 2, 1),
        2: Project(2, "P2", "d", "2030-01-01", 5, 0),
    }
    applications = [
        Application(1, projects[1], user, "t", "active"),
        Application(2, projects[1], user, "t", "cancelled"),
    ]
    stats = app_mod.get_statistics(projects, applications)
    assert stats["total_projects"] == 2
    assert stats["total_places"] == 7
    assert stats["taken_places"] == 1
    assert stats["free_places"] == 6
    assert stats["active_applications"] == 1
    assert stats["cancelled_applications"] == 1


def test_get_statistics_empty():
    stats = app_mod.get_statistics({}, [])
    assert stats["total_projects"] == 0
    assert stats["fill_percent"] == 0.0

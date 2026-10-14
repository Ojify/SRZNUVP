import domain_projects as proj_mod
from domain_projects import Project


def test_project_creation_and_str():
    p = Project(1, "Космос", "Полёт на Марс", "2030-01-01", 3, 1)
    assert p.id == 1
    assert p.name == "Космос"
    assert p.max_participants == 3
    assert p.current_participants == 1
    assert "свободно: 2" in str(p)


def test_is_available_and_free_places():
    p = Project(1, "X", "d", "2030-01-01", 3, 1)
    assert p.is_available() is True
    assert p.free_places() == 2

    p2 = Project(2, "X", "d", "2030-01-01", 2, 2)
    assert p2.is_available() is False
    assert p2.free_places() == 0


def test_check_availability_and_free_places_helpers():
    p = Project(1, "X", "d", "2030-01-01", 3, 1)
    assert proj_mod.check_availability(p) is True
    assert proj_mod.free_places(p) == 2
    assert proj_mod.check_availability(None) is False
    assert proj_mod.free_places(None) == 0


def test_project_from_data_and_to_data():
    p = Project.from_data({
        "id": 5, "name": "P", "description": "d",
        "deadline": "2030-01-01",
        "max_participants": 4, "current_participants": 2,
    })
    assert p.id == 5
    assert p.max_participants == 4
    assert p.to_data()["current_participants"] == 2


def test_projects_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setattr("storage.DATA_DIR", str(tmp_path))
    projects = {
        1: Project(1, "A", "d", "2030-01-01", 5, 0),
        2: Project(2, "B", "d", "2031-01-01", 3, 2),
    }
    proj_mod.save_projects(projects)
    loaded = proj_mod.load_projects()
    assert [p.name for p in loaded.values()] == ["A", "B"]
    assert loaded[2].current_participants == 2
    assert isinstance(loaded[1], Project)


def test_add_edit_delete_project(tmp_path, monkeypatch):
    monkeypatch.setattr("storage.DATA_DIR", str(tmp_path))
    projects = {}
    pid = proj_mod.add_project(
        projects, "X", "d", "2030-01-01", 3
    )
    assert pid in projects
    assert proj_mod.find_project(projects, pid) is projects[pid]

    assert proj_mod.edit_project(
        projects, pid, name="Y", max_participants=10
    ) is True
    assert projects[pid].name == "Y"
    assert projects[pid].max_participants == 10

    assert proj_mod.edit_project(projects, 999, name="Z") is False

    assert proj_mod.delete_project(projects, pid) is True
    assert projects == {}


def test_search_projects(tmp_path, monkeypatch):
    monkeypatch.setattr("storage.DATA_DIR", str(tmp_path))
    projects = {
        1: Project(1, "Космос", "Полёт на Марс",
                   "2030-01-01", 2, 0),
        2: Project(2, "Роботы", "Сборка роботов",
                   "2027-05-05", 5, 1),
    }
    assert [
        p.id for p in proj_mod.search_projects(projects, "косм")
    ] == [1]
    assert [
        p.id for p in proj_mod.search_projects(projects, "робот")
    ] == [2]
    assert len(proj_mod.search_projects(projects, "")) == 2


def test_sort_projects(tmp_path, monkeypatch):
    monkeypatch.setattr("storage.DATA_DIR", str(tmp_path))
    projects = {
        1: Project(1, "Космос", "d", "2030-01-01", 2, 0),
        2: Project(2, "Роботы", "d", "2027-05-05", 5, 1),
    }
    assert [
        p.id for p in proj_mod.sort_projects(projects, "name")
    ] == [1, 2]
    assert [
        p.id for p in proj_mod.sort_projects(
            projects, "deadline", reverse=True
        )
    ] == [1, 2]

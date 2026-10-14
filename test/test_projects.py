import pytest

import domain_projects as proj


@pytest.fixture
def sample_projects():
    return {
        1: {
            "id": 1, "name": "Космос", "description": "Полёт на Марс",
            "deadline": "2030-01-01", "max_participants": 2,
            "current_participants": 0,
        },
        2: {
            "id": 2, "name": "Роботы", "description": "Сборка роботов",
            "deadline": "2027-05-05", "max_participants": 5,
            "current_participants": 1,
        },
    }


def test_check_availability_true(sample_projects):
    assert proj.check_availability(sample_projects[2]) is True


def test_check_availability_false(sample_projects):
    sample_projects[1]["current_participants"] = 2
    assert proj.check_availability(sample_projects[1]) is False


def test_free_places(sample_projects):
    assert proj.free_places(sample_projects[1]) == 2
    assert proj.free_places(sample_projects[2]) == 4


def test_add_project(sample_projects):
    pid = proj.add_project(sample_projects, "Тест", "Описание", "2030-12-31", 3)
    assert pid == 3
    assert sample_projects[3]["name"] == "Тест"
    assert sample_projects[3]["current_participants"] == 0


def test_edit_project(sample_projects):
    ok = proj.edit_project(sample_projects, 1, name="Новое", max_participants=10)
    assert ok is True
    assert sample_projects[1]["name"] == "Новое"
    assert sample_projects[1]["max_participants"] == 10


def test_edit_project_not_found(sample_projects):
    assert proj.edit_project(sample_projects, 999, name="X") is False


def test_delete_project(sample_projects):
    assert proj.delete_project(sample_projects, 1) is True
    assert 1 not in sample_projects


def test_search_projects_by_name(sample_projects):
    result = proj.search_projects(sample_projects, "косм")
    assert len(result) == 1
    assert result[0]["id"] == 1


def test_search_projects_by_description(sample_projects):
    result = proj.search_projects(sample_projects, "робот")
    assert len(result) == 1
    assert result[0]["id"] == 2


def test_search_projects_empty_query(sample_projects):
    assert len(proj.search_projects(sample_projects, "")) == 2


def test_sort_projects_by_name(sample_projects):
    ids = [p["id"] for p in proj.sort_projects(sample_projects, "name")]
    assert ids == [1, 2]


def test_sort_projects_by_deadline_desc(sample_projects):
    ids = [p["id"] for p in proj.sort_projects(sample_projects, "deadline", reverse=True)]
    assert ids == [1, 2]


def test_projects_roundtrip(tmp_path, monkeypatch, sample_projects):
    monkeypatch.setattr("storage.DATA_DIR", str(tmp_path))
    proj.save_projects(sample_projects)
    loaded = proj.load_projects()
    assert loaded == sample_projects
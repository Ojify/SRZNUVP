"""Тесты для main.py (запуск: pytest -v)."""

import pytest

import main as app


@pytest.fixture
def sample_projects():
    return {
        1: {
            "id": 1,
            "name": "Космос",
            "description": "Полёт на Марс",
            "deadline": "2030-01-01",
            "max_participants": 2,
            "current_participants": 0,
        },
        2: {
            "id": 2,
            "name": "Роботы",
            "description": "Сборка роботов",
            "deadline": "2027-05-05",
            "max_participants": 5,
            "current_participants": 1,
        },
    }


@pytest.fixture
def sample_bookings():
    return [
        {"id": 1, "project_id": 2, "user_name": "Аня",
         "created_at": "2025-01-01T10:00:00", "status": "active"},
        {"id": 2, "project_id": 2, "user_name": "Борис",
         "created_at": "2025-01-02T10:00:00", "status": "cancelled"},
    ]


# ---------- Работа с файлами ----------

def test_load_projects_missing_file(tmp_path):
    assert app.load_projects(str(tmp_path / "nope.json")) == {}


def test_load_bookings_missing_file(tmp_path):
    assert app.load_bookings(str(tmp_path / "nope.json")) == []


def test_projects_roundtrip(tmp_path, sample_projects):
    path = str(tmp_path / "projects.json")
    app.save_projects(sample_projects, path)
    assert app.load_projects(path) == sample_projects


def test_bookings_roundtrip(tmp_path, sample_bookings):
    path = str(tmp_path / "bookings.json")
    app.save_bookings(sample_bookings, path)
    assert app.load_bookings(path) == sample_bookings


def test_load_corrupted_json(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text("{not a json", encoding="utf-8")
    assert app.load_projects(str(path)) == {}
    assert app.load_bookings(str(path)) == []


# ---------- ID ----------

def test_next_project_id(sample_projects):
    assert app.next_project_id(sample_projects) == 3
    assert app.next_project_id({}) == 1


def test_next_booking_id(sample_bookings):
    assert app.next_booking_id(sample_bookings) == 3
    assert app.next_booking_id([]) == 1


# ---------- Доступность ----------

def test_check_availability_true(sample_projects):
    assert app.check_availability(sample_projects[2]) is True


def test_check_availability_false(sample_projects):
    sample_projects[1]["current_participants"] = 2
    assert app.check_availability(sample_projects[1]) is False


def test_free_places(sample_projects):
    assert app.free_places(sample_projects[1]) == 2
    assert app.free_places(sample_projects[2]) == 4


# ---------- CRUD проектов ----------

def test_add_project(sample_projects):
    pid = app.add_project(sample_projects, "Тест", "Описание", "2030-12-31", 3)
    assert pid == 3
    assert sample_projects[3]["name"] == "Тест"
    assert sample_projects[3]["current_participants"] == 0
    assert sample_projects[3]["max_participants"] == 3


def test_edit_project(sample_projects):
    ok = app.edit_project(sample_projects, 1, name="Новое", max_participants=10)
    assert ok is True
    assert sample_projects[1]["name"] == "Новое"
    assert sample_projects[1]["max_participants"] == 10


def test_edit_project_not_found(sample_projects):
    assert app.edit_project(sample_projects, 999, name="X") is False


def test_delete_project_removes_bookings(sample_projects, sample_bookings):
    assert app.delete_project(sample_projects, sample_bookings, 2) is True
    assert 2 not in sample_projects
    assert all(b["project_id"] != 2 for b in sample_bookings)


# ---------- Бронирования ----------

def test_add_booking_success(sample_projects, sample_bookings):
    booking, msg = app.add_booking(sample_bookings, sample_projects, 1, "Иван")
    assert booking is not None
    assert booking["status"] == "active"
    assert sample_projects[1]["current_participants"] == 1
    assert "добавлена" in msg.lower()


def test_add_booking_project_not_found(sample_projects, sample_bookings):
    booking, msg = app.add_booking(sample_bookings, sample_projects, 999, "Иван")
    assert booking is None
    assert "не найден" in msg.lower()


def test_add_booking_no_places(sample_projects, sample_bookings):
    sample_projects[1]["current_participants"] = sample_projects[1]["max_participants"]
    booking, msg = app.add_booking(sample_bookings, sample_projects, 1, "Иван")
    assert booking is None
    assert "мест" in msg.lower()


def test_add_booking_duplicate(sample_projects, sample_bookings):
    app.add_booking(sample_bookings, sample_projects, 1, "Иван")
    booking, msg = app.add_booking(sample_bookings, sample_projects, 1, "иван")
    assert booking is None
    assert "уже" in msg.lower()


def test_cancel_booking(sample_projects, sample_bookings):
    ok, msg = app.cancel_booking(sample_bookings, sample_projects, 1)
    assert ok is True
    assert sample_bookings[0]["status"] == "cancelled"
    assert sample_projects[2]["current_participants"] == 0


def test_cancel_booking_twice(sample_projects, sample_bookings):
    app.cancel_booking(sample_bookings, sample_projects, 1)
    ok, msg = app.cancel_booking(sample_bookings, sample_projects, 1)
    assert ok is False
    assert "уже" in msg.lower()


def test_cancel_booking_not_found(sample_projects, sample_bookings):
    ok, msg = app.cancel_booking(sample_bookings, sample_projects, 999)
    assert ok is False
    assert "не найдена" in msg.lower()


# ---------- Поиск и сортировка ----------

def test_search_projects_by_name(sample_projects):
    result = app.search_projects(sample_projects, "косм")
    assert len(result) == 1
    assert result[0]["id"] == 1


def test_search_projects_by_description(sample_projects):
    result = app.search_projects(sample_projects, "робот")
    assert len(result) == 1
    assert result[0]["id"] == 2


def test_search_projects_empty_query(sample_projects):
    assert len(app.search_projects(sample_projects, "")) == 2


def test_sort_projects_by_name(sample_projects):
    ids = [p["id"] for p in app.sort_projects(sample_projects, "name")]
    assert ids == [1, 2]  # "Космос" < "Роботы"


def test_sort_projects_by_deadline_desc(sample_projects):
    ids = [p["id"] for p in app.sort_projects(sample_projects, "deadline", reverse=True)]
    assert ids == [1, 2]


# ---------- Статистика ----------

def test_get_statistics(sample_projects, sample_bookings):
    stats = app.get_statistics(sample_projects, sample_bookings)
    assert stats["total_projects"] == 2
    assert stats["total_places"] == 7
    assert stats["taken_places"] == 1
    assert stats["free_places"] == 6
    assert stats["active_bookings"] == 1
    assert stats["cancelled_bookings"] == 1
    assert stats["fill_percent"] == round(1 / 7 * 100, 2)


def test_get_statistics_empty():
    stats = app.get_statistics({}, [])
    assert stats["total_projects"] == 0
    assert stats["fill_percent"] == 0.0
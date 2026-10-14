"""Сервис регистрации заявок на участие в проектах."""

import domain_applications as app_mod
import domain_projects as proj_mod
import domain_statuses as status_mod
import domain_users as user_mod
from utils import parse_date, parse_int, parse_positive_int, parse_skills


def print_projects(items):
    if not items:
        print("Список проектов пуст.\n")
        return
    print("\n--- Проекты ---")
    for p in items:
        print(f"[{p['id']}] {p['name']}  "
              f"({p['current_participants']}/{p['max_participants']}, "
              f"свободно: {proj_mod.free_places(p)})")
        print(f"    Описание: {p['description']}")
        print(f"    Дедлайн:  {p['deadline']}")
    print("--------------\n")


def print_users(users):
    if not users:
        print("Пользователей нет.\n")
        return
    print("\n--- Пользователи ---")
    for u in users.values():
        skills = ", ".join(u.get("skills", [])) or "—"
        print(f"[{u['id']}] {u['name']} <{u['email']}>  навыки: {skills}")
    print("--------------------\n")


def print_applications(applications, projects, users, statuses):
    if not applications:
        print("Заявок нет.\n")
        return
    print("\n--- Заявки ---")
    for a in applications:
        project = projects.get(a["project_id"])
        user = users.get(a["user_id"])
        pname = project["name"] if project else "(проект удалён)"
        uname = user["name"] if user else "(пользователь удалён)"
        sname = statuses.get(a["status"], {}).get("name", a["status"])
        print(f"[{a['id']}] {uname} → «{pname}»  статус: {sname}  ({a['created_at']})")
    print("--------------\n")


def print_statuses(statuses):
    print("\n--- Справочник статусов ---")
    for s in statuses.values():
        print(f"[{s['code']}] {s['name']} — {s['description']}")
    print("---------------------------\n")


def menu():
    projects = proj_mod.load_projects()
    users = user_mod.load_users()
    applications = app_mod.load_applications()
    statuses = status_mod.load_statuses()
    status_mod.save_statuses(statuses)

    while True:
        print("========= Меню =========")
        print("1. Показать все проекты")
        print("2. Показать проект по ID")
        print("3. Добавить проект")
        print("4. Редактировать проект")
        print("5. Удалить проект")
        print("6. Проверить доступность проекта")
        print("7. Поиск проектов")
        print("8. Сортировка проектов")
        print("9. Пользователи: список")
        print("10. Пользователи: добавить")
        print("11. Пользователи: редактировать")
        print("12. Пользователи: удалить")
        print("13. Пользователи: поиск")
        print("14. Статусы: справочник")
        print("15. Подать заявку")
        print("16. Отменить заявку")
        print("17. Показать все заявки")
        print("18. Статистика")
        print("0. Выход")
        print("========================")
        choice = input("Выберите пункт: ").strip()

        if choice == "0":
            proj_mod.save_projects(projects)
            user_mod.save_users(users)
            app_mod.save_applications(applications)
            status_mod.save_statuses(statuses)
            print("Данные сохранены. Выход.")
            break

        elif choice == "1":
            print_projects(list(projects.values()))

        elif choice == "2":
            pid = _read_int("Введите ID проекта: ")
            if pid is None:
                continue
            p = proj_mod.find_project(projects, pid)
            if p is None:
                print(f"Проект с ID {pid} не найден.\n")
            else:
                print_projects([p])

        elif choice == "3":
            name = input("Название: ").strip()
            if not name:
                print("Ошибка: название пустое.\n")
                continue
            description = input("Описание: ").strip()
            if not description:
                print("Ошибка: описание пустое.\n")
                continue
            deadline = _read_date("Дедлайн (yyyy-mm-dd): ")
            if not deadline:
                continue
            max_p = _read_positive_int("Максимум участников: ")
            if max_p is None:
                continue
            pid = proj_mod.add_project(projects, name, description, deadline, max_p)
            proj_mod.save_projects(projects)
            print(f"Проект добавлен. ID: {pid}\n")

        elif choice == "4":
            print_projects(list(projects.values()))
            pid = _read_int("ID проекта для редактирования: ")
            if pid is None or pid not in projects:
                print("Проект не найден.\n")
                continue
            name = input("Новое название (Enter — пропустить): ").strip() or None
            description = input("Новое описание (Enter — пропустить): ").strip() or None
            deadline_raw = input("Новый дедлайн (Enter — пропустить): ").strip()
            deadline = None
            if deadline_raw:
                try:
                    deadline = parse_date(deadline_raw)
                except ValueError:
                    print("Дедлайн не изменён: неверный формат.")
            max_raw = input("Новый максимум (Enter — пропустить): ").strip()
            max_value = None
            if max_raw:
                try:
                    max_value = parse_positive_int(max_raw)
                except ValueError:
                    print("Максимум не изменён.")
            proj_mod.edit_project(projects, pid, name, description, deadline, max_value)
            proj_mod.save_projects(projects)
            print("Проект обновлён.\n")

        elif choice == "5":
            print_projects(list(projects.values()))
            pid = _read_int("ID проекта для удаления: ")
            if pid is None or pid not in projects:
                print("Проект не найден.\n")
                continue
            confirm = input(f"Удалить «{projects[pid]['name']}»? (y/n): ").strip().lower()
            if confirm == "y":
                proj_mod.delete_project(projects, pid)
                applications[:] = [a for a in applications if a["project_id"] != pid]
                proj_mod.save_projects(projects)
                app_mod.save_applications(applications)
                print("Проект удалён.\n")
            else:
                print("Отменено.\n")

        elif choice == "6":
            print_projects(list(projects.values()))
            pid = _read_int("ID проекта для проверки: ")
            if pid is None:
                continue
            p = proj_mod.find_project(projects, pid)
            if p is None:
                print("Проект не найден.\n")
            elif proj_mod.check_availability(p):
                print(f"Доступен. Свободно мест: {proj_mod.free_places(p)}.\n")
            else:
                print("Недоступен: свободных мест нет.\n")

        elif choice == "7":
            query = input("Введите подстроку: ").strip()
            found = proj_mod.search_projects(projects, query)
            print(f"Найдено: {len(found)}")
            print_projects(found)

        elif choice == "8":
            print("Ключ: 1) id  2) name  3) deadline  4) participants")
            key_map = {"1": "id", "2": "name", "3": "deadline", "4": "participants"}
            key = key_map.get(input("Выбор: ").strip(), "name")
            reverse = input("По убыванию? (y/n): ").strip().lower() == "y"
            print_projects(proj_mod.sort_projects(projects, key, reverse))

        elif choice == "9":
            print_users(users)

        elif choice == "10":
            name = input("Имя: ").strip()
            if not name:
                print("Ошибка: имя пустое.\n")
                continue
            email = input("Email: ").strip()
            if not email:
                print("Ошибка: email пустой.\n")
                continue
            skills = parse_skills(input("Навыки через запятую (можно пусто): "))
            uid = user_mod.add_user(users, name, email, skills)
            user_mod.save_users(users)
            print(f"Пользователь добавлен. ID: {uid}\n")

        elif choice == "11":
            print_users(users)
            uid = _read_int("ID пользователя для редактирования: ")
            if uid is None or uid not in users:
                print("Пользователь не найден.\n")
                continue
            name = input("Новое имя (Enter — пропустить): ").strip() or None
            email = input("Новый email (Enter — пропустить): ").strip() or None
            skills_raw = input("Новые навыки (Enter — пропустить): ").strip()
            skills = parse_skills(skills_raw) if skills_raw else None
            user_mod.edit_user(users, uid, name, email, skills)
            user_mod.save_users(users)
            print("Пользователь обновлён.\n")

        elif choice == "12":
            print_users(users)
            uid = _read_int("ID пользователя для удаления: ")
            if uid is None or uid not in users:
                print("Пользователь не найден.\n")
                continue
            confirm = input(f"Удалить «{users[uid]['name']}»? (y/n): ").strip().lower()
            if confirm == "y":
                user_mod.delete_user(users, uid)
                applications[:] = [a for a in applications if a["user_id"] != uid]
                user_mod.save_users(users)
                app_mod.save_applications(applications)
                print("Пользователь удалён.\n")
            else:
                print("Отменено.\n")

        elif choice == "13":
            query = input("Введите подстроку: ").strip()
            found = user_mod.search_users(users, query)
            print(f"Найдено: {len(found)}")
            for u in found:
                skills = ", ".join(u.get("skills", [])) or "—"
                print(f"[{u['id']}] {u['name']} <{u['email']}>  навыки: {skills}")
            print()

        elif choice == "14":
            print_statuses(statuses)

        elif choice == "15":
            if not projects or not users:
                print("Нужны хотя бы один проект и один пользователь.\n")
                continue
            print_projects(list(projects.values()))
            pid = _read_int("ID проекта: ")
            if pid is None:
                continue
            print_users(users)
            uid = _read_int("ID пользователя: ")
            if uid is None:
                continue
            project = proj_mod.find_project(projects, pid)
            user = user_mod.find_user(users, uid)
            application, msg = app_mod.add_application(applications, project, user)
            proj_mod.save_projects(projects)
            app_mod.save_applications(applications)
            print(msg + "\n")

        elif choice == "16":
            print_applications(applications, projects, users, statuses)
            aid = _read_int("ID заявки для отмены: ")
            if aid is None:
                continue
            application = app_mod.find_application(applications, aid)
            project = projects.get(application["project_id"]) if application else None
            ok, msg = app_mod.cancel_application(applications, project, aid)
            proj_mod.save_projects(projects)
            app_mod.save_applications(applications)
            print(msg + "\n")

        elif choice == "17":
            print_applications(applications, projects, users, statuses)

        elif choice == "18":
            stats = app_mod.get_statistics(projects, applications)
            print("\n--- Статистика ---")
            print(f"Всего проектов:      {stats['total_projects']}")
            print(f"Активных заявок:     {stats['active_applications']}")
            print(f"Отменённых заявок:   {stats['cancelled_applications']}")
            print(f"Всего мест:          {stats['total_places']}")
            print(f"Занято мест:         {stats['taken_places']}")
            print(f"Свободно мест:       {stats['free_places']}")
            print(f"Заполненность:       {stats['fill_percent']}%\n")

        else:
            print("Неизвестная команда.\n")


def _read_int(prompt):
    raw = input(prompt).strip()
    try:
        return parse_int(raw)
    except ValueError:
        print("Ошибка: нужно целое число.")
        return None


def _read_positive_int(prompt):
    raw = input(prompt).strip()
    try:
        return parse_positive_int(raw)
    except ValueError:
        print("Ошибка: нужно целое число > 0.")
        return None


def _read_date(prompt):
    raw = input(prompt).strip()
    try:
        return parse_date(raw)
    except ValueError:
        print("Ошибка: неверный формат даты.")
        return None


if __name__ == "__main__":
    menu()
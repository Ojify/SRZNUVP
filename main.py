from datetime import datetime

projects = {}
next_id = 1

while True:
    print("========= Меню =========")
    print("1. Показать все проекты")
    print("2. Показать проект по ID")
    print("3. Добавить проект")
    print("4. Редактировать проект")
    print("5. Удалить проект")
    print("0. Выход")
    print("========================")
    choice = input("Выберите пункт: ").strip()

    if choice == "0":
        print("Выход из программы.")
        break

    elif choice == "1":
        if not projects:
            print("Список проектов пуст.\n")
        else:
            print("\n--- Список проектов ---")
            for p in projects.values():
                print(f"[{p['id']}] {p['name']}")
                print(f"    Описание: {p['description']}")
                print(f"    Дедлайн:  {p['deadline']}")
                print(f"    Участники: {p['current_participants']}/{p['max_participants']}")
            print("-----------------------\n")

    elif choice == "2":
        if not projects:
            print("Список проектов пуст.\n")
            continue
        for p in projects.values():
            print(f"[{p['id']}] {p['name']}")
        try:
            pid = int(input("Введите ID проекта: ").strip())
        except ValueError:
            print("Ошибка: нужно целое число.\n")
            continue
        p = projects.get(pid)
        if not p:
            print(f"Проект с ID {pid} не найден.\n")
        else:
            print(f"\nID: {p['id']}")
            print(f"Название: {p['name']}")
            print(f"Описание: {p['description']}")
            print(f"Дедлайн: {p['deadline']}")
            print(f"Участники: {p['current_participants']}/{p['max_participants']}\n")

    elif choice == "3":
        print("\n--- Добавление проекта ---")
        name = input("Название: ").strip()
        if not name:
            print("Ошибка: название не может быть пустым.\n")
            continue
        description = input("Описание: ").strip()
        if not description:
            print("Ошибка: описание не может быть пустым.\n")
            continue
        try:
            deadline = datetime.strptime(input("Дедлайн (yyyy-mm-dd): ").strip(), "%Y-%m-%d").date()
        except ValueError:
            print("Ошибка: неверный формат даты.\n")
            continue
        try:
            max_participants = int(input("Максимум участников: ").strip())
            if max_participants <= 0:
                print("Ошибка: число должно быть больше нуля.\n")
                continue
        except ValueError:
            print("Ошибка: нужно целое число.\n")
            continue

        projects[next_id] = {
            "id": next_id,
            "name": name,
            "description": description,
            "deadline": deadline,
            "max_participants": max_participants,
            "current_participants": 0,
        }
        print(f"Проект добавлен. ID: {next_id}\n")
        next_id += 1

    elif choice == "4":
        if not projects:
            print("Список проектов пуст — нечего редактировать.\n")
            continue
        for p in projects.values():
            print(f"[{p['id']}] {p['name']}")
        try:
            pid = int(input("Введите ID проекта для редактирования: ").strip())
        except ValueError:
            print("Ошибка: нужно целое число.\n")
            continue
        if pid not in projects:
            print(f"Проект с ID {pid} не найден.\n")
            continue

        p = projects[pid]
        print("Оставьте поле пустым, чтобы не изменять его.")
        name = input("Новое название: ").strip()
        description = input("Новое описание: ").strip()
        deadline_raw = input("Новый дедлайн (yyyy-mm-dd): ").strip()
        max_raw = input("Новый максимум участников: ").strip()

        if name:
            p["name"] = name
        if description:
            p["description"] = description
        if deadline_raw:
            try:
                p["deadline"] = datetime.strptime(deadline_raw, "%Y-%m-%d").date()
            except ValueError:
                print("Дедлайн не изменён: неверный формат даты.")
        if max_raw:
            try:
                value = int(max_raw)
                if value > 0:
                    p["max_participants"] = value
                else:
                    print("Максимум участников не изменён: число должно быть > 0.")
            except ValueError:
                print("Максимум участников не изменён: нужно целое число.")
        print("Проект обновлён.\n")

    elif choice == "5":
        if not projects:
            print("Список проектов пуст — нечего удалять.\n")
            continue
        for p in projects.values():
            print(f"[{p['id']}] {p['name']}")
        try:
            pid = int(input("Введите ID проекта для удаления: ").strip())
        except ValueError:
            print("Ошибка: нужно целое число.\n")
            continue
        if pid not in projects:
            print(f"Проект с ID {pid} не найден.\n")
            continue
        confirm = input(f"Удалить проект «{projects[pid]['name']}»? (y/n): ").strip().lower()
        if confirm == "y":
            del projects[pid]
            print("Проект удалён.\n")
        else:
            print("Удаление отменено.\n")

    else:
        print("Неизвестная команда. Попробуйте снова.\n")
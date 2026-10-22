import json
from db.database import get_connection


def load_json(filename):
    with open(filename, encoding="utf-8") as f:
        return json.load(f)


def main():
    conn = get_connection()
    try:
        # Очистка таблиц перед импортом
        conn.executescript("""
            DELETE FROM applications;
            DELETE FROM projects;
            DELETE FROM users;
            DELETE FROM statuses;
        """)

        # 1. Статусы
        statuses = load_json("data/statuses.json")
        conn.executemany(
            "INSERT INTO statuses (code, name, description) VALUES (?, ?, ?)",
            [(k, v['name'], v['description']) for k, v in statuses.items()]
        )

        # 2. Пользователи (навыки объединяем в строку)
        users = load_json("data/users.json")
        users_data = []
        for k, v in users.items():
            skills_str = ", ".join(v.get('skills', []))
            users_data.append((int(k), v['name'], v['email'], skills_str))
        conn.executemany(
            "INSERT INTO users (id, name, email, skills) VALUES (?, ?, ?, ?)",
            users_data
        )

        # 3. Проекты
        projects = load_json("data/projects.json")
        projects_data = []
        for k, v in projects.items():
            projects_data.append((
                int(k), v['name'], v['description'], v['deadline'],
                v['max_participants'], v['current_participants']
            ))
        conn.executemany(
            """INSERT INTO projects 
               (id, name, description, deadline, max_participants, current_participants) 
               VALUES (?, ?, ?, ?, ?, ?)""",
            projects_data
        )

        # 4. Заявки
        applications = load_json("data/applications.json")
        if applications:
            applications_data = [
                (a['id'], a['project_id'], a['user_id'], a['created_at'], a['status'])
                for a in applications
            ]
            conn.executemany(
                """INSERT INTO applications 
                   (id, project_id, user_id, created_at, status) 
                   VALUES (?, ?, ?, ?, ?)""",
                applications_data
            )

        conn.commit()
        print("--- Импорт успешно завершен! ---")
    except Exception as e:
        conn.rollback()
        print(f"ОШИБКА ПРИ ИМПОРТЕ: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()

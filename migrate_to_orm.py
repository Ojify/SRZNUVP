import os
import sys
import sqlite3
from datetime import datetime
from pathlib import Path
import django

BASE_DIR = Path(__file__).resolve().parent.parent if "__file__" in locals() else Path.cwd()
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from projects.models import Project
from users.models import User
from applications.models import Application, Status

SOURCE_DB = BASE_DIR / "data" / "srznuvp.sqlite"

def main():
    if not SOURCE_DB.exists():
        print(f"Файл {SOURCE_DB} не найден!")
        return

    with sqlite3.connect(SOURCE_DB) as conn:
        conn.row_factory = sqlite3.Row

        # 1. Статусы
        statuses = conn.execute("SELECT * FROM statuses").fetchall()
        for row in statuses:
            Status.objects.update_or_create(
                code=row["code"],
                defaults={"name": row["name"], "description": row["description"]}
            )

        # 2. Пользователи
        users = conn.execute("SELECT * FROM users").fetchall()
        for row in users:
            User.objects.update_or_create(
                id=row["id"],
                defaults={
                    "name": row["name"],
                    "email": row["email"],
                    "skills": row["skills"] or ""
                }
            )

        # 3. Проекты
        projects = conn.execute("SELECT * FROM projects").fetchall()
        for row in projects:
            Project.objects.update_or_create(
                id=row["id"],
                defaults={
                    "name": row["name"],
                    "description": row["description"],
                    "deadline": row["deadline"],
                    "max_participants": row["max_participants"],
                    "current_participants": row["current_participants"]
                }
            )

        # 4. Заявки
        applications = conn.execute("SELECT * FROM applications").fetchall()
        for row in applications:
            # Преобразуем строку в datetime
            created_at = datetime.fromisoformat(row["created_at"]) if row["created_at"] else datetime.now()
            Application.objects.update_or_create(
                id=row["id"],
                defaults={
                    "project_id": row["project_id"],
                    "user_id": row["user_id"],
                    "created_at": created_at,
                    "status_id": row["status"]
                }
            )

    print("--- Данные успешно перенесены в Django ORM! ---")

if __name__ == "__main__":
    main()

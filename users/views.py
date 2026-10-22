import sqlite3
from django.shortcuts import render

DB_PATH = "data/srznuvp.sqlite"


def users(request):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    users_list = conn.execute("""
        SELECT id, name, email, skills FROM users ORDER BY name;
    """).fetchall()
    conn.close()
    return render(request, 'users/user_list.html', {'users_list': users_list})


def user_detail(request, user_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    user = conn.execute("""
        SELECT id, name, email, skills FROM users WHERE id = ?;
    """, (user_id,)).fetchone()

    if user is None:
        conn.close()
        return render(request, 'users/user_detail.html', {'user': None}, status=404)

    user_applications = conn.execute("""
        SELECT a.id, a.status, p.name AS project_name
        FROM applications a
        JOIN projects p ON a.project_id = p.id
        WHERE a.user_id = ?;
    """, (user_id,)).fetchall()
    conn.close()

    return render(request, 'users/user_detail.html', {
        'user': user,
        'user_applications': user_applications
    })

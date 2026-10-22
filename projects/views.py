import sqlite3
from django.shortcuts import render

DB_PATH = "data/srznuvp.sqlite"


def projects(request):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    projects_list = conn.execute("""
        SELECT id, name, deadline, max_participants, current_participants 
        FROM projects ORDER BY deadline;
    """).fetchall()
    conn.close()
    return render(request, 'projects/project_list.html', {'projects_list': projects_list})


def project_detail(request, project_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    
    # Вычисляем свободные места и сразу передаем в шаблон
    project = conn.execute("""
        SELECT id, name, description, deadline, max_participants, current_participants,
               (max_participants - current_participants) AS free_places
        FROM projects WHERE id = ?;
    """, (project_id,)).fetchone()

    if project is None:
        conn.close()
        return render(request, 'projects/project_detail.html', {'project': None}, status=404)

    # Получаем заявки на этот проект (JOIN)
    project_applications = conn.execute("""
        SELECT a.id, a.created_at, a.status, u.name AS user_name
        FROM applications a
        JOIN users u ON a.user_id = u.id
        WHERE a.project_id = ?;
    """, (project_id,)).fetchall()
    conn.close()

    return render(request, 'projects/project_detail.html', {
        'project': project,
        'project_applications': project_applications
    })

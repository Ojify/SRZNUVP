import sqlite3
from django.shortcuts import render

DB_PATH = "data/srznuvp.sqlite"


def applications(request):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    applications_list = conn.execute("""
        SELECT a.id, a.created_at, a.status,
               p.name AS project_name, 
               u.name AS user_name
        FROM applications a
        JOIN projects p ON a.project_id = p.id
        JOIN users u ON a.user_id = u.id
        ORDER BY a.created_at DESC;
    """).fetchall()
    conn.close()
    return render(request, 'applications/application_list.html', {'applications_list': applications_list})


def application_detail(request, application_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Добавляем JOIN со статусами для получения description
    application = conn.execute("""
        SELECT a.id, a.created_at, a.status,
               p.id AS project_id, p.name AS project_name, 
               u.id AS user_id, u.name AS user_name,
               s.description AS status_desc
        FROM applications a
        JOIN projects p ON a.project_id = p.id
        JOIN users u ON a.user_id = u.id
        LEFT JOIN statuses s ON a.status = s.code
        WHERE a.id = ?;
    """, (application_id,)).fetchone()
    
    if application is None:
        conn.close()
        return render(request, 'applications/application_detail.html', {'application': None}, status=404)
        
    conn.close()
    return render(request, 'applications/application_detail.html', {'application': application})


def statistics(request):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    
    # COALESCE превращает None в 0, чтобы избежать ошибки TypeError
    stats_row = conn.execute("""
        SELECT 
            (SELECT COUNT(*) FROM projects) AS total_projects,
            (SELECT COUNT(*) FROM applications WHERE status = 'active') AS active_apps,
            (SELECT COUNT(*) FROM applications WHERE status = 'cancelled') AS cancelled_apps,
            COALESCE((SELECT SUM(max_participants) FROM projects), 0) AS total_places,
            COALESCE((SELECT SUM(current_participants) FROM projects), 0) AS taken_places
    """).fetchone()
    conn.close()

    stats = dict(stats_row)
    stats['free_places'] = max(0, stats['total_places'] - stats['taken_places'])
    stats['fill_percent'] = round(stats['taken_places'] / stats['total_places'] * 100, 2) if stats['total_places'] else 0

    return render(request, 'applications/statistics.html', {'stats': stats})

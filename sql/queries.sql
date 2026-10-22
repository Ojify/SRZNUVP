-- 1. Список всех проектов (SELECT)
SELECT id, name, deadline, max_participants, current_participants FROM projects ORDER BY deadline;

-- 2. Список всех пользователей (SELECT)
SELECT id, name, email, skills FROM users ORDER BY name;

-- 3. Проекты, где есть свободные места (WHERE)
SELECT id, name, max_participants - current_participants AS free_places 
FROM projects 
WHERE current_participants < max_participants;

-- 4. Активные заявки (WHERE)
SELECT id, project_id, user_id, created_at 
FROM applications 
WHERE status = 'active';

-- 5. Детальная информация о заявках (JOIN)
SELECT a.id, a.created_at, a.status,
       p.name AS project_name, 
       u.name AS user_name
FROM applications a
JOIN projects p ON a.project_id = p.id
JOIN users u ON a.user_id = u.id
ORDER BY a.created_at DESC;

-- 6. Пользователи и названия проектов, на которые они подали заявки (JOIN)
SELECT u.name AS user_name, p.name AS project_name, a.status
FROM applications a
JOIN users u ON a.user_id = u.id
JOIN projects p ON a.project_id = p.id;

-- 7. Общее количество пользователей (COUNT)
SELECT COUNT(*) AS total_users FROM users;

-- 8. Количество активных заявок (COUNT + WHERE)
SELECT COUNT(*) AS active_applications FROM applications WHERE status = 'active';

-- 9. Статистика заявок по статусам (GROUP BY)
SELECT status, COUNT(*) AS count
FROM applications
GROUP BY status;

-- 10. Популярные проекты (больше 1 заявки) (GROUP BY + HAVING)
SELECT p.name AS project_name, COUNT(a.id) AS applications_count
FROM projects p
JOIN applications a ON p.id = a.project_id
GROUP BY p.id, p.name
HAVING COUNT(a.id) > 1;

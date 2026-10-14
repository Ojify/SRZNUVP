from django.http import HttpResponse

from homepage.views import page
from domain_applications import (
    find_application,
    get_statistics,
    load_applications,
)
from domain_projects import load_projects
from domain_users import load_users
from domain_statuses import load_statuses


def applications(request):
    applications_list = load_applications()
    projects = load_projects()
    users_dict = load_users()
    statuses = load_statuses()

    items = ''
    for a in applications_list:
        project = projects.get(a['project_id'])
        user = users_dict.get(a['user_id'])
        pname = project['name'] if project else '(проект удалён)'
        uname = user['name'] if user else '(пользователь удалён)'
        sname = statuses.get(a['status'], {}).get('name', a['status'])

        badge = 'bg-success' if a['status'] == 'active' else 'bg-secondary'

        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/applications/{a['id']}/">
                [{a['id']}] {uname} → «{pname}»
            </a>
            <span class="badge {badge}">{sname}</span>
        </li>
        """

    content = f"""
    <h1>Заявки</h1>
    <p>Всего заявок: {len(applications_list)}</p>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page('Заявки', content))


def application_detail(request, application_id):
    applications_list = load_applications()
    application = find_application(applications_list, application_id)

    if application is None:
        content = """
        <h1 class="text-danger">Заявка не найдена</h1>
        <a href="/applications/"
           class="btn btn-outline-secondary">← к списку заявок</a>
        """
        return HttpResponse(
            page('Заявка не найдена', content),
            status=404,
        )

    projects = load_projects()
    users_dict = load_users()
    statuses = load_statuses()

    project = projects.get(application['project_id'])
    user = users_dict.get(application['user_id'])
    status = statuses.get(application['status'], {})

    project_link = (
        f'<a href="/projects/{project["id"]}/">{project["name"]}</a>'
        if project else '(проект удалён)'
    )
    user_link = (
        f'<a href="/users/{user["id"]}/">{user["name"]}</a>'
        if user else '(пользователь удалён)'
    )

    badge = 'bg-success' if application['status'] == 'active' else 'bg-secondary'
    status_name = status.get('name', application['status'])
    status_desc = status.get('description', '')

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Заявка №{application['id']}</h5>
            <p class="card-text"><strong>Проект:</strong> {project_link}</p>
            <p class="card-text"><strong>Пользователь:</strong> {user_link}</p>
            <p class="card-text"><strong>Создана:</strong> {application['created_at']}</p>
            <p class="card-text">
                <strong>Статус:</strong>
                <span class="badge {badge}">{status_name}</span>
                — {status_desc}
            </p>
        </div>
    </div>
    <a href="/applications/"
       class="btn btn-outline-secondary mt-3">← к списку заявок</a>
    """
    return HttpResponse(page(f'Заявка №{application["id"]}', content))


def statistics(request):
    projects = load_projects()
    applications_list = load_applications()
    stats = get_statistics(projects, applications_list)

    content = f"""
    <h1>Статистика</h1>
    <ul class="list-group">
        <li class="list-group-item">Всего проектов: {stats['total_projects']}</li>
        <li class="list-group-item">Активных заявок: {stats['active_applications']}</li>
        <li class="list-group-item">Отменённых заявок: {stats['cancelled_applications']}</li>
        <li class="list-group-item">Всего мест: {stats['total_places']}</li>
        <li class="list-group-item">Занято мест: {stats['taken_places']}</li>
        <li class="list-group-item">Свободно мест: {stats['free_places']}</li>
        <li class="list-group-item">Заполненность: {stats['fill_percent']}%</li>
    </ul>
    """
    return HttpResponse(page('Статистика', content))

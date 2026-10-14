from django.http import HttpResponse

from homepage.views import page
from domain_projects import (
    find_project,
    free_places,
    load_projects,
)
from domain_applications import load_applications


def projects(request):
    projects_dict = load_projects()
    items = ''
    for p in projects_dict.values():
        items += f"""
        <li class="list-group-item">
            <a href="/projects/{p['id']}/">
                [{p['id']}] {p['name']}
                — {p['current_participants']}/{p['max_participants']},
                свободно: {free_places(p)}
            </a>
        </li>
        """
    content = f"""
    <h1>Проекты</h1>
    <p>Всего проектов: {len(projects_dict)}</p>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page('Проекты', content))


def project_detail(request, project_id):
    projects_dict = load_projects()
    project = find_project(projects_dict, project_id)

    if project is None:
        content = """
        <h1 class="text-danger">Проект не найден</h1>
        <a href="/projects/"
           class="btn btn-outline-secondary">← к списку проектов</a>
        """
        return HttpResponse(
            page('Проект не найден', content),
            status=404,
        )

    applications = load_applications()
    project_applications = [
        a for a in applications if a['project_id'] == project_id
    ]

    status = 'доступен' if free_places(project) > 0 else 'мест нет'
    badge = 'bg-success' if free_places(project) > 0 else 'bg-danger'

    rows = ''
    for a in project_applications:
        rows += f"""
        <li class="list-group-item">
            <a href="/applications/{a['id']}/">Заявка №{a['id']}</a>
            — статус: {a['status']} ({a['created_at']})
        </li>
        """

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{project['name']}</h5>
            <p class="card-text"><strong>Описание:</strong> {project['description']}</p>
            <p class="card-text"><strong>Дедлайн:</strong> {project['deadline']}</p>
            <p class="card-text">
                <strong>Участников:</strong>
                {project['current_participants']} из {project['max_participants']}
            </p>
            <p class="card-text">
                Статус: <span class="badge {badge}">{status}</span>
            </p>
        </div>
    </div>
    <h2 class="mt-4">Заявки на проект</h2>
    <ul class="list-group">{rows}</ul>
    <a href="/projects/"
       class="btn btn-outline-secondary mt-3">← к списку проектов</a>
    """
    return HttpResponse(page(project['name'], content))
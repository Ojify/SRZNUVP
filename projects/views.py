from django.shortcuts import render

from domain_projects import find_project, load_projects
from domain_users import load_users
from domain_applications import load_applications


def projects(request):
    """Список проектов."""
    projects_dict = load_projects()
    context = {
        "projects": list(projects_dict.values()),
    }
    return render(request, "projects/project_list.html", context)


def project_detail(request, project_id):
    """Карточка проекта и заявки на него."""
    projects_dict = load_projects()
    project = find_project(projects_dict, project_id)

    project_applications = []
    if project is not None:
        users_dict = load_users()
        applications = load_applications(projects_dict, users_dict)
        project_applications = [
            a for a in applications if a.project.id == project_id
        ]

    context = {
        "project": project,
        "project_applications": project_applications,
    }
    return render(
        request,
        "projects/project_detail.html",
        context,
        status=404 if project is None else 200,
    )

from django.shortcuts import render

from domain_applications import (
    find_application,
    get_statistics,
    load_applications,
)
from domain_projects import load_projects
from domain_users import load_users
from domain_statuses import load_statuses


def _attach_statuses(applications, statuses):
    """Подложить каждой заявке атрибут status_obj.

    Django Template Language не позволяет обращаться к словарю
    по динамическому ключу, поэтому объект Status передаётся
    в шаблон через атрибут заявки.
    """
    for a in applications:
        a.status_obj = statuses.get(a.status)
    return applications


def applications(request):
    """Список заявок."""
    projects = load_projects()
    users_dict = load_users()
    applications_list = load_applications(projects, users_dict)
    statuses = load_statuses()
    _attach_statuses(applications_list, statuses)

    context = {
        "applications": applications_list,
    }
    return render(request, "applications/application_list.html", context)


def application_detail(request, application_id):
    """Карточка заявки."""
    projects = load_projects()
    users_dict = load_users()
    applications_list = load_applications(projects, users_dict)
    application = find_application(applications_list, application_id)

    if application is not None:
        statuses = load_statuses()
        application.status_obj = statuses.get(application.status)

    context = {
        "application": application,
    }
    return render(
        request,
        "applications/application_detail.html",
        context,
        status=404 if application is None else 200,
    )


def statistics(request):
    """Статистика по проектам и заявкам."""
    projects = load_projects()
    users_dict = load_users()
    applications_list = load_applications(projects, users_dict)
    stats = get_statistics(projects, applications_list)

    context = {
        "stats": stats,
    }
    return render(request, "applications/statistics.html", context)

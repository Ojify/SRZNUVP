from django.shortcuts import render

from domain_users import find_user, load_users
from domain_projects import load_projects
from domain_applications import load_applications


def users(request):
    """Список пользователей."""
    users_dict = load_users()
    context = {
        "users": list(users_dict.values()),
    }
    return render(request, "users/user_list.html", context)


def user_detail(request, user_id):
    """Карточка пользователя и его заявки."""
    users_dict = load_users()
    user = find_user(users_dict, user_id)

    user_applications = []
    if user is not None:
        projects = load_projects()
        applications = load_applications(projects, users_dict)
        user_applications = [
            a for a in applications if a.user.id == user_id
        ]

    context = {
        "user": user,
        "user_applications": user_applications,
    }
    return render(
        request,
        "users/user_detail.html",
        context,
        status=404 if user is None else 200,
    )

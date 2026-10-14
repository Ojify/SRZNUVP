from django.http import HttpResponse

from homepage.views import page
from domain_users import find_user, load_users
from domain_projects import load_projects
from domain_applications import load_applications


def users(request):
    users_dict = load_users()
    items = ''
    for u in users_dict.values():
        skills = ', '.join(u.skills) or '—'
        items += f"""
        <li class="list-group-item">
            <a href="/users/{u.id}/">
                [{u.id}] {u.name} &lt;{u.email}&gt;
                — навыки: {skills}
            </a>
        </li>
        """
    content = f"""
    <h1>Пользователи</h1>
    <p>Всего пользователей: {len(users_dict)}</p>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page('Пользователи', content))


def user_detail(request, user_id):
    users_dict = load_users()
    user = find_user(users_dict, user_id)

    if user is None:
        content = """
        <h1 class="text-danger">Пользователь не найден</h1>
        <a href="/users/"
           class="btn btn-outline-secondary">← к списку пользователей</a>
        """
        return HttpResponse(
            page('Пользователь не найден', content),
            status=404,
        )

    projects = load_projects()
    applications = load_applications(projects, users_dict)
    user_applications = [
        a for a in applications if a.user.id == user_id
    ]

    skills = ', '.join(user.skills) or '—'

    rows = ''
    for a in user_applications:
        rows += f"""
        <li class="list-group-item">
            <a href="/applications/{a.id}/">Заявка №{a.id}</a>
            — проект «{a.project.name}», статус: {a.status}
        </li>
        """

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{user.name}</h5>
            <p class="card-text"><strong>Email:</strong> {user.email}</p>
            <p class="card-text"><strong>Навыки:</strong> {skills}</p>
        </div>
    </div>
    <h2 class="mt-4">Заявки пользователя</h2>
    <ul class="list-group">{rows}</ul>
    <a href="/users/"
       class="btn btn-outline-secondary mt-3">← к списку пользователей</a>
    """
    return HttpResponse(page(user.name, content))

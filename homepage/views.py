from django.http import HttpResponse

BOOTSTRAP_CSS = (
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3'
    '/dist/css/bootstrap.min.css'
)


def page(title: str, content: str) -> str:
    """Единый HTML-каркас для всех страниц проекта."""
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{BOOTSTRAP_CSS}">
</head>
<body>
    <nav class="nav bg-light mb-4 px-3 py-2">
        <a class="nav-link" href="/">Главная</a>
        <a class="nav-link" href="/projects/">Проекты</a>
        <a class="nav-link" href="/users/">Пользователи</a>
        <a class="nav-link" href="/applications/">Заявки</a>
        <a class="nav-link" href="/applications/statistics/">Статистика</a>
    </nav>
    <main class="container">{content}</main>
</body>
</html>"""


def index(request):
    content = """
    <h1 class="display-4">Сервис заявок на проекты</h1>
    <p class="lead">Удобный интерфейс для поиска проектов и регистрации
    заявок на участие.</p>
    <p>Основные разделы:</p>
    <a href="/projects/" class="btn btn-primary me-2">Проекты</a>
    <a href="/users/" class="btn btn-primary me-2">Пользователи</a>
    <a href="/applications/" class="btn btn-secondary me-2">Заявки</a>
    <a href="/applications/statistics/" class="btn btn-info">Статистика</a>
    """
    return HttpResponse(page('Сервис заявок', content))


def page_not_found(request, exception):
    content = """
    <h1 class="text-danger">404 — страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page('404 — страница не найдена', content),
        status=404,
    )
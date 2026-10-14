from django.shortcuts import render


def index(request):
    """Главная страница."""
    return render(request, "homepage/index.html")


def page_not_found(request, exception):
    """Собственная страница 404.

    Вызывается Django при DEBUG=False вместо технической страницы.
    Параметр exception обязателен: Django передаёт в него объект
    исключения, приведшего к ошибке 404.
    """
    return render(
        request,
        "404.html",
        status=404,
    )

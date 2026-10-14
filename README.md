# Сервис регистрации заявок на участие в проектах

Веб-приложение на Django для поиска проектов и регистрации заявок
на участие в них. Консольная версия сохранена и работает параллельно
с веб-интерфейсом.

## Используемые технологии

- Python 3;
- Django 5.2 — веб-фреймворк;
- Django Template Language (DTL);
- HTML5, CSS3, JavaScript;
- Bootstrap 5.3 (через CDN);
- JSON — хранение данных;
- pytest — автоматизированные тесты;
- flake8 — проверка качества кода;
- Git.

## Предметная область

Основные сущности:

- **Проект (Project)** — инициатива, в которую подаются заявки;
- **Пользователь (User)** — физическое лицо, подающее заявку;
- **Заявка (Application)** — запрос пользователя на участие;
- **Статус (Status)** — справочник состояний заявки
  (`active`, `cancelled`, `approved`, `rejected`).

Один пользователь не может иметь две активные заявки на один проект.
Отменённая заявка не блокирует повторную подачу.

## Веб-страницы

| Страница | URL | View-функция | Шаблон |
|---|---|---|---|
| Главная | `/` | `homepage.views.index` | `homepage/index.html` |
| Проекты | `/projects/` | `projects.views.projects` | `projects/project_list.html` |
| Проект | `/projects/<id>/` | `projects.views.project_detail` | `projects/project_detail.html` |
| Пользователи | `/users/` | `users.views.users` | `users/user_list.html` |
| Пользователь | `/users/<id>/` | `users.views.user_detail` | `users/user_detail.html` |
| Заявки | `/applications/` | `applications.views.applications` | `applications/application_list.html` |
| Заявка | `/applications/<id>/` | `applications.views.application_detail` | `applications/application_detail.html` |
| Статистика | `/applications/statistics/` | `applications.views.statistics` | `applications/statistics.html` |

Страницы проектов, пользователей и заявок возвращают код **404** и
собственную страницу ошибки, если объект с указанным идентификатором
не найден.

## Django Template Language

### Базовый шаблон и наследование

Общий каркас страниц — `templates/base.html`. Он содержит:

- объявление HTML-документа и `<head>`;
- подключение Bootstrap и собственного `style.css`;
- логотип и навигацию (`{% include "includes/navigation.html" %}`);
- подвал с текущим годом;
- подключение собственного `main.js`;
- два блока: `{% block title %}` и `{% block content %}`.

Дочерние шаблоны используют `{% extends "base.html" %}` и переопределяют
эти блоки.

### Включаемые шаблоны

Повторяющиеся фрагменты вынесены через `{% include %}`:

- `templates/includes/navigation.html` — навигационное меню;
- `users/templates/users/includes/user_card.html` — карточка пользователя;
- `projects/templates/projects/includes/project_card.html` — карточка проекта;
- `applications/templates/applications/includes/application_status.html`
  — бейдж статуса заявки.

### Контекст

Каждая view-функция подготавливает словарь `context` и передаёт его в
`render(request, "шаблон.html", context)`. В шаблонах данные доступны
по именам ключей: `{{ project.name }}`, `{{ user.email }}`,
`{{ application.created_at }}`.

### Циклы и условия

- Циклы: `{% for project in projects %} ... {% empty %} ... {% endfor %}`.
- Условия: `{% if project.is_available %} ... {% else %} ... {% endif %}`.
- Пустые коллекции обрабатываются через `{% empty %}` (списки) и
  `{% else %}` (детальные страницы).

### Именованные URL и пространства имён

В каждом `urls.py` определён `app_name`, у маршрутов есть параметр `name`.
Ссылки в шаблонах формируются через `{% url %}`:

```html
{% url 'projects:list' %}
{% url 'projects:detail' project.id %}
{% url 'applications:statistics' %}
```

Жёсткие адреса в шаблонах не используются.

### Фильтры шаблонов

| Фильтр | Где применяется |
|---|---|
| `length` | `{{ projects\|length }}`, `{{ users\|length }}` — количество элементов |
| `default` | `{{ user.name\|default:"Без имени" }}` — значение по умолчанию |
| `join` | `{{ user.skills\|join:", " }}` — список через запятую |
| `truncatechars` | `{{ project.description\|truncatechars:120 }}` — обрезка описания |

## Статические файлы

Структура:

```
homepage/static/homepage/
├── css/style.css
├── js/main.js
└── img/logo.png
```

Подключение в `base.html`:

```html
{% load static %}
<link rel="stylesheet" href="{% static 'homepage/css/style.css' %}">
<img src="{% static 'homepage/img/logo.png' %}" alt="Сервис заявок">
<script src="{% static 'homepage/js/main.js' %}"></script>
```

- `style.css` — собственные стили проекта поверх Bootstrap;
- `main.js` — подставляет текущий год в подвал и подсвечивает
  активный пункт навигации;
- `logo.png` — логотип проекта, отображается в шапке.

## Хранение данных

Данные хранятся в JSON-файлах в каталоге `data/`:

- `data/projects.json`;
- `data/users.json`;
- `data/applications.json`;
- `data/statuses.json`.

Загрузка и сохранение — через модуль `storage.py`. Доменные объекты
(`Project`, `User`, `Application`, `Status`) создаются в `domain_*.py`.
Django ORM и база данных пока не используются — переход на них
запланирован в следующих практических работах.

## Структура проекта

```
SRZNUVP-main/
├── manage.py
├── main.py                  # консольная версия
├── storage.py
├── utils.py
├── requirements.txt
├── .flake8
├── .gitignore
├── README.md
│
├── config/                  # настройки Django-проекта
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── templates/               # общие шаблоны
│   ├── base.html
│   ├── 404.html
│   └── includes/
│       └── navigation.html
│
├── homepage/
│   ├── templates/homepage/index.html
│   ├── static/homepage/
│   │   ├── css/style.css
│   │   ├── js/main.js
│   │   └── img/logo.png
│   ├── views.py
│   └── urls.py
│
├── projects/
│   ├── templates/projects/
│   │   ├── project_list.html
│   │   ├── project_detail.html
│   │   └── includes/project_card.html
│   ├── views.py
│   └── urls.py
│
├── users/
│   ├── templates/users/
│   │   ├── user_list.html
│   │   ├── user_detail.html
│   │   └── includes/user_card.html
│   ├── views.py
│   └── urls.py
│
├── applications/
│   ├── templates/applications/
│   │   ├── application_list.html
│   │   ├── application_detail.html
│   │   ├── statistics.html
│   │   └── includes/application_status.html
│   ├── views.py
│   └── urls.py
│
├── domain_projects.py
├── domain_users.py
├── domain_applications.py
├── domain_statuses.py
│
├── data/
│   ├── projects.json
│   ├── users.json
│   ├── applications.json
│   └── statuses.json
│
└── tests/
    ├── test_projects.py
    ├── test_users.py
    └── test_applications.py
```

## Запуск

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Открыть в браузере: `http://127.0.0.1:8000/`.

Консольная версия:

```bash
python main.py
```

## Тестирование и качество кода

```bash
pytest -v
flake8 .
```

## Текущее состояние и план развития

### Реализовано (ПР1–ПР6)

- Объектная модель предметной области (`Project`, `User`, `Application`, `Status`);
- Консольное приложение (`main.py`);
- JSON-хранилище (`storage.py`, `data/`);
- Django-проект и четыре приложения;
- Маршрутизация URL, именованные маршруты, пространства имён;
- View-функции на `render()`;
- Собственная обработка ошибки 404;
- Django Template Language: `extends`, `block`, `include`, `for`, `if`,
  `empty`, фильтры (`length`, `default`, `join`, `truncatechars`);
- Ссылки через `{% url %}`;
- Собственные статические файлы (CSS, JS, PNG);
- Bootstrap 5.3 через CDN;
- Тесты и проверка кода (`pytest`, `flake8`).

### Планируется

- Перенос сущностей в Django ORM и подключение базы данных;
- Формы Django для создания, редактирования и удаления объектов;
- Аутентификация и регистрация пользователей;
- Разработка API;
- Контейнеризация;
- CI/CD.

[![.github/workflows/yamdb_workflow.yml](https://github.com/admiration91/foodgram-project-react/actions/workflows/main.yml/badge.svg)](https://github.com/admiration91/foodgram-project-react/actions/workflows/main.yml)
# Foodgram Project

# IP рабочего сервера - 51.250.71.62

## Описание

Приложение "Продуктовый помощник" это сайт, на котором пользователи могут публиковать свои рецепты, добавлять понравившиеся рецепты других пользователей в избранное и подписываться на их публикации. Также, можно воспользоваться сервисом "Список покупок", которые позволяет составлять перечень продуктов, которые необходимо купить для приготовления любимых блюд.

У каждого рецепта можно выбрать один или несколько тэгов. Например "завтрак" или "вкусно" и фильтровать необходимы рецепты по ним.

Понравившиеся рецепты можно добавить в избранное. На любимых авторов рецептов можно подписаться и отслеживать все их рецепты.

Для публикации рецептов, работы со списком избранного или списком покупок необходимо авторизоваться. Неавторизованные пользователи могу только просматривать рецепты или страницы других пользователей.

### Алгоритм регистрации пользователей
1. Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами `email`, `username`, `first_name`, `last_name`, `password` на эндпоинт `/api/users/`.
2. Пользователь получает токен аутентификации, отправляя POST-запрос со своими `email` и `password` на эндпоинт `/api/auth/token/login/`.

## Используемые технологии и библиотеки
-   [Python >= 3.7](https://www.python.org/)
-   [Django = 3.2](https://www.djangoproject.com/)
-   [djangorestframework = 3.12.4](https://www.django-rest-framework.org/)
-   [djoser = 2.1.0](https://djoser.readthedocs.io/en/latest/getting_started.html)
-   [requests = 2.26.0](https://requests.readthedocs.io/en/latest/user/quickstart/)
-   [pytest = 6.2.4](https://docs.pytest.org/en/7.1.x/getting-started.html)
-   [pytest-django = 4.4.0](https://pytest-django.readthedocs.io/en/latest/tutorial.html)
-   [pytest-pythonpath = 0.7.3](https://pypi.org/project/pytest-pythonpath/)
-   [django-import-export = 3.0.2](https://django-import-export.readthedocs.io/en/latest/getting_started.html)
-   [django-filter = 22.1](https://django-filter.readthedocs.io/)
-   [gunicorn==20.0.4](https://docs.gunicorn.org/en/stable/settings.html)
-   [psycopg2-binary==2.8.6](https://www.psycopg.org/docs/)
-   [reportlab==3.6.12](https://docs.reportlab.com/)
-   [gunicorn==20.0.4](https://github.com/benoitc/gunicorn)
-   [nginx==1.19.3](https://nginx.org/ru/docs/)
-   [django-filter](https://django-filter.readthedocs.io/en/stable/)


При необходимости есть возможность наполнить БД данными из CSV файлов. Импорт осуществляется с помощью management команды. Необходимо прописать `python manage.py load_database`.

## Документация
Документация находится по адресу `http://127.0.0.1:8000/api/redoc/`.


## Примеры запросов к API

### Авторизация

Регистрация нового пользователя:
```POST
http://51.250.71.62//api/users/
```
payload:
```application/json
{
  "email": "user@example.com",
  "username": "string"
  "first_name": "monty"
  "last_name": "python"
  "password": "eggs"
}
```

Получение токена:
```POST
http://51.250.71.62//api/auth/token/login/
```
payload:
```application/json
{
  "email": "string",
  "password": "eggs"
}
```

#### Рецепты

Получение списка рецептов
```GET
http://51.250.71.62//api/recipes/
```

Получение конкретного рецепта
```GET
http://51.250.71.62//api/recipes/{id}/
```

Создание рецепта
```POST
http://51.250.71.62//api/recipes/
```
payload:
```application/json
"ingredients": [
{
"id": 1123,
"amount": 10
}
],
"tags": [
1,
2
],
"image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
"name": "string",
"text": "string",
"cooking_time": 1
}
```
### Тэги
Получение списка тэгов
```GET
http://51.250.71.62//api/tags/
```

Получение тэга
```GET
http://51.250.71.62//api/tags/{id}
```

### Избранное

Добавить рецепт в избранное
```POST
http://51.250.71.62//api/recipes/{id}/favorite
```

Посмотреть список избранного
```GET
http://51.250.71.62//api/favorites
```

### Пользователи

Посмотреть список пользователей
```GET
http://51.250.71.62//api/users/
```

Посмотреть конкретного пользователя
```GET
http://51.250.71.62//api/users/{id}
```

### Подписки

Подписаться на пользователя
```POST
http://51.250.71.62//api/users/{id}
```

Посмотреть список подписок
```GET
http://51.250.71.62//api/users/subscriptions
```

#### Список покупок
Скачать список покупой
```GET
http://127.0.0.1:8000/api/recipes/download_shopping_cart/
```
